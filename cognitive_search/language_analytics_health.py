import imp
from azure.ai.textanalytics import (TextAnalyticsClient)
from azure.core.credentials import AzureKeyCredential
from article import *

import os
from dotenv import load_dotenv
import sys

sys.path.append("../thesis_code")

from cosmos_db_gremlin import graph_cosmos_gremlin

load_dotenv()


def apply_text_analytics(article_list, separate):
    # authenticate client
    client = authenticate_client()

    #all_graph(article_list, client)

    #graph_cosmos_gremlin.powershell_create_graphs(len(article_list))

    
    for index in range(len(article_list)):
        graph_name = "art_" + str(index)
        article_graph(article_list[index], separate, client, graph_name)


    #article_graph(article_list[1], separate, client)
    #print(article_list[1].all)




def article_graph(article, separate, client, graph_name):

    if separate:
        text_list = []
        
        text_list.append(article.methods)  
        text_list.append(article.results)  
        text_list.append(article.discussion)  
        text_list.append(article.conclusion)          

        docs = health_relations(client, text_list)
    else:        
        docs = health_relations(client, [article.all])

    graph_cosmos_gremlin.create_graph(docs, graph_name)

    



def all_graph(conclusion_list, client):
    text_list = []

    for i in range(len(conclusion_list)):
        text_list.append(conclusion_list[i].conclusion)  # <-- set on conclusion at the moment

    #print(conclusion_list[-1])

    docs = health_relations(client, text_list)

    #print_docs(docs)

    # conclusions, art0-4
    graph_name = "conclusions"

    graph_cosmos_gremlin.create_graph(docs, graph_name)


# authenticate client in order to use the text analytics services
def authenticate_client():
    language_key = os.getenv('LANGUAGE_ADMIN_API_KEY')
    language_endpoint = os.getenv('LANGUAGE_ENDPOINT')

    ta_credential = AzureKeyCredential(language_key)
    ta_client = TextAnalyticsClient(
        endpoint=language_endpoint,
        credential=ta_credential
    )
    return ta_client



# extract health relations from text
def health_relations(client, text_list):
    documents = text_list

    poller = client.begin_analyze_healthcare_entities(documents)
    result = poller.result()

    docs = [doc for doc in result if not doc.is_error]
    return docs





def print_docs(docs):
    for idx, doc in enumerate(docs):
        print("\n\n DOCUMENT " + str(idx))
        '''
        for entity in doc.entities:
            print("Entity: {} ---".format(entity.text))
            print("...Normalized Text: {}".format(entity.normalized_text))
            print("...Category: {}".format(entity.category))
            print("...Subcategory: {}".format(entity.subcategory))
            print("...Offset: {}".format(entity.offset))
            print("...Confidence score: {}".format(entity.confidence_score))
        '''
        print("----------------------------")
        for relation in doc.entity_relations:
            print("Relation of type: {} has the following roles".format(relation.relation_type))
            for role in relation.roles:
                print("...Role '{}' with entity '{}'".format(role.name, role.entity.text))
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("------------------------------------------")




