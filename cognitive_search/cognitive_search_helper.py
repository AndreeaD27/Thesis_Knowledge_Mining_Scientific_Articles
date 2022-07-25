import encodings
import os
from re import L
from unittest import result
from dotenv import load_dotenv
import os
from pprint import pprint # pretty printer
import requests

from cognitive_search_components import *
from language_analytics_health import apply_text_analytics
from article import *

'''
Access indexes and retrieve content and title
Continue with applying Health Text Analytics
'''
def search_content(endpoint, headers, params, index_name):

    '''
    for experimental purposes:
        section_separation=True when we do section separation
        section_separation=False when we retrieve the content of the entire article without separating into section
    '''
    section_separation = True

    time.sleep(10)  # <- NOTE: if no results are returned from the request, increase the time of sleeping before doing the request
    r = requests.get(endpoint + "/indexes/" + index_name + "/docs?&search=*&$count=true&$select=content", headers=headers, params=params)
    t = requests.get(endpoint + "/indexes/" + index_name + "/docs?&search=*&$count=true&$select=title", headers=headers, params=params)
    
    result_json = r.json()
    title_json = t.json()
    
    document_count = result_json["@odata.count"] # <-- retrieves the number of documents in the index

    json_list = []
    title_list = []

    'Extract the content and title per each document'
    for i in range(document_count):
        json_list.append(result_json["value"][i])  # <-- result_json["value"][i] is the content that we are looking for per each document
        title_list.append(title_json["value"][i]['title'])

     
    if section_separation:
        article_list_section_separated = create_article_list_separated(json_list, title_list)    
        apply_text_analytics(article_list_section_separated, section_separation)
    else:
        article_list_no_separation = create_article_list_not_separated(json_list, title_list)
        apply_text_analytics(article_list_no_separation, section_separation)


'''
Create list of objects of Article type
Section (e.g. results, conclusion) attributes remain empty.
'''
def create_article_list_not_separated(contents, titles):
    size = len(contents)
    article_list = []

    for i in range(size):
        all = extract_section(contents[i], "All")
        article = Article(all=all, title=titles[i])
        article_list.append(article)

    return article_list

'''
Create list of objects of Article type
Section (e.g. results, conclusion) attributes are populated with extracted sections.
'''
def create_article_list_separated(contents, titles):
    size = len(contents)
    article_list = []

    for i in range(size):
        article = create_article(contents[i], titles[i])
        article_list.append(article)

    return article_list


'''
Extracts specific sections per article and creates object
'''
def create_article(content, title):
   
    methods = extract_section(content, "Methods")
    results = extract_section(content, "Results")
    discussion = extract_section(content, "Discussion")
    conclusion = extract_section(content, "Conclusion") 

    article = Article(methods, results, discussion, conclusion, title)

    return article