import logging
import azure.functions as func
import json
import re #regex

# https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-python


'''
@input: http request
@output: http response

Receive a request and return a reponse containing a json the extracted section
'''
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # if there is no json sent through the request
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid body",
            status_code=400
        )

    if body:
        result = compose_response(body)
        return func.HttpResponse(
            result, 
            mimetype="application/json"
        )
    else:
        return func.HttpResponse(
            "Invalid body",
            status_code=400
        )

'''
@input: a json object
@output: a dictionary as a string

Organize the result from the extract_section(body) function as a dictionary
so that it can be used in the http response
'''
def compose_response(body:json) -> str:
    #prepare the output json
    results = {}
  
    section, section_lowerletter_name  = find_section_names_extract(body)

    if section != None:
        results[section_lowerletter_name] = []
        results[section_lowerletter_name].append(section)
    else:
        results[section_lowerletter_name] = []
        raise ValueError("The  cannot be null!")

    return json.dumps(results, ensure_ascii=False)

'''
@input: json object containing article 
@output: extracted section and standardized section name in lowercase

Set initial standard section names. Extract requested section. Requested section found in body["section"]
'''
def find_section_names_extract(body:json) -> str:

    content = body["content"]
    section_name = body["section"]
    next_section_name = ""

    all = False
    ## Standardized
    if section_name == "Introduction":
        next_section_name = "Methods"
    elif section_name == "Methods":
        next_section_name = "Results"
    elif section_name == "Results":
        next_section_name = "Discussion"
    elif section_name == "Discussion":
        next_section_name = "Conclusion"
    elif section_name == "Conclusion":
        next_section_name = "Acknowledgements"
    elif section_name == "All":
        section_name = "Introduction"
        next_section_name = "Acknowledgements"
        all = True

    # We do not use the new_section_name (variation; _) because we want to keep it standardized
    section, _ = extract_section(section_name=section_name, next_section_name=next_section_name, content=content, all=all)

    return section, section_name.lower()
        
'''
@input: section_name - current section name, next_section_name - next section name, content - content of the entire article
@output: a section of the json object as a string

Extract the content from the json object. Extract the section from the text. 
'''    
def extract_section(section_name:str, next_section_name: str, content: str, all: bool) -> str:    
    
    regex_terms = set_regex(section_name, next_section_name)

    content = clean_content(content)

    # Return the section (including the current section name and the next section name); None if section not found
    result = re.search(regex_terms, content)    
    
    # Recursive steps: try with variations of section names
    if result == None:
        variation_current_section_name = variation_current_section(section_name)
        if variation_current_section_name != None:
          result, section_name = extract_section(variation_current_section_name, next_section_name, content, all)
    
        variation_next_section_name = variation_next_section(section_name, next_section_name, all)
        if result == None and variation_next_section_name != None:
            result, section_name = extract_section(section_name, variation_next_section_name, content, all)

    else:
        result = clean_result(result,section_name, next_section_name)

    # Base case
    if result == None:
        return "Section NOT FOUND!", section_name.lower()

    return result, section_name.lower()

'''
@input: section_name - current section name
@output: variation of the current section name

Take into consideration the variations of the same section name

Note: arrange the if statements in the order of priority (most restrictive to less restrictive)
'''
def variation_current_section(section_name:str) -> str:

    variation_section_name = None
    
    if section_name == "Methods":
        variation_section_name = "Materials and Methods"

    if section_name == "Materials and Methods":
        variation_section_name = "Materials and methods"

    if section_name == "Materials and methods":
        variation_section_name = "Material and methods"

    if section_name == "Material and methods":
        variation_section_name = "Subjects and methods"

    if section_name == "Introduction":
        variation_section_name = ""

    return variation_section_name

'''
@input: section_name - current section name, next_section_name - next section name
@output: variation of the next section name

Take into consideration the variations of the next section name

Note: arrange the if statements in the order of priority (most restrictive to less restrictive)
'''
def variation_next_section(section_name:str, next_section_name:str, all:bool) -> str:

    variation_next_section_name = None

    if section_name == "Introduction":

        # Renaming Methods
        if next_section_name == "Methods":
            variation_next_section_name = "Materials and Methods"

        if next_section_name == "Materials and Methods":
            variation_next_section_name = "Materials and methods"

        if next_section_name == "Materials and methods":
            variation_next_section_name = "Material and methods"

    if section_name == "Conclusion" or all:

        if next_section_name == "Acknowledgements":
            variation_next_section_name = "Compliance with ethical standards "

        if next_section_name == "Compliance with ethical standards ":
            variation_next_section_name = "Source of funding"

        if next_section_name == "Source of funding":
            variation_next_section_name = "Supporting information"    
        
        if next_section_name == "Supporting information":
            variation_next_section_name = "Reference"

        if next_section_name == "Reference":
            variation_next_section_name = "References"

    return variation_next_section_name

'''
Set different regex depending on sections
'''
def set_regex(section_name, next_section_name):
    # Regex to identify a section. A section has to start with the name of the current section and end with the name of the next section
    
    if next_section_name == "Acknowledgements":
        regex_terms = r'\n('+section_name+r')\n(.|\n)+\n'+next_section_name
    else: 
        regex_terms = r'\n('+section_name+r')\n(.|\n)+\n('+next_section_name+r')\n' 

    return regex_terms
    
'''
Clean the result depending on section name
'''
def clean_result(result, section_name, next_section_name):

    res_a = result[0]    
    
    # Remove the section names

    res_b = res_a.replace("\n"+section_name+"\n", "")

    if next_section_name == "Acknowledgements":
        res = res_b.replace("\n"+next_section_name, "")
    else:
        res = res_b.replace("\n"+next_section_name+"\n", "")

    return res

'''
Clean content in order for regex search to find correct matches
'''
def clean_content(content):

    content = content.replace(u'\xa0', u' ')

    return content
