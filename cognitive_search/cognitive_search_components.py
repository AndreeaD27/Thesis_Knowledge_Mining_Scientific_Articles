import json
import requests
import time
import os
from dotenv import load_dotenv

'''

'''
def clear_previous_resources(endpoint, headers, params, datasource_name, skillset_name, index_name, indexer_name):
    print("clearing resources")
    r = requests.delete(endpoint + "/datasources/" + datasource_name,
                    headers=headers, params=params)
    print(r.status_code)

    r = requests.delete(endpoint + "/skillsets/" + skillset_name,
                        headers=headers, params=params)
    print(r.status_code)

    r = requests.delete(endpoint + "/indexes/" + index_name,
                        headers=headers, params=params)
    print(r.status_code)

    r = requests.delete(endpoint + "/indexers/" + indexer_name,
                        headers=headers, params=params)
    print(r.status_code)


'''

'''
def create_datasource(endpoint, headers, params, datasource_name):

    load_dotenv()

    datasource_connection_string = os.getenv('STORAGE_CONNECTION_STRING')
    blob_container_name = os.getenv('CONTAINER_NAME')

    datasource_payload = {
        "name": datasource_name,
        "description": "Article examples",
        "type" : "azureblob",
        "credentials": {
            "connectionString": datasource_connection_string
        },
        "container": {
            "name": blob_container_name
        }    
    }

    r = requests.put(endpoint + "/datasources/" + datasource_name, 
                    data=json.dumps(datasource_payload), headers=headers, params=params)

    print("creating datasource")
    print(r.status_code)


'''

'''
def create_skillset(endpoint, headers, params, skillset_name):

    language_detection_skill = {
                "@odata.type": "#Microsoft.Skills.Text.LanguageDetectionSkill",
                "inputs": [
                    {
                        "name": "text", 
                        "source": "/document/content"
                    }
                ],
                "outputs": [
                    {
                        "name": "languageCode",
                        "targetName": "languageCode"
                    }
                ]
            } 

    text_split_skill = {
                "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
                "textSplitMode": "pages",
                "maximumPageLength": 4000,
                "inputs": [
                    {
                        "name": "text",
                        "source": "/document/content"
                    },
                    {
                        "name": "languageCode",
                        "source": "/document/languageCode"
                    }
                ],
                "outputs": [
                    {
                        "name": "textItems",
                        "targetName": "pages"
                    }
                ]
            }

    key_phrase_extraction_skill = {
                "@odata.type": "#Microsoft.Skills.Text.KeyPhraseExtractionSkill",
                "context": "/document/pages/*",
                "inputs": [
                    {
                        "name": "text", 
                        "source": "/document/pages/*"
                    },
                    {
                        "name": "languageCode", 
                        "source": "/document/languageCode"
                    }
                ],
                "outputs": [
                    {
                        "name": "keyPhrases",
                        "targetName": "keyPhrases"
                    }
                ]
            }


    skill_list = [language_detection_skill, text_split_skill]

    skillset_payload = {
        "name": skillset_name,
        "description": "Detect language, split text and extract key-phrases",
        "skills": skill_list    
    }

    r = requests.put(endpoint + "/skillsets/" + skillset_name,
                    data=json.dumps(skillset_payload), headers=headers, params=params)
                    
    print("creating skillset")
    print(r.status_code)


'''

'''
def create_field(name:str, type:str, searchable="false", filterable="false", sortable="false", facetable="false", key="false") -> dict:
    field = {
        "name": name,
        "type": type,
        "key": key,
        "searchable": searchable,
        "filterable": filterable,
        "sortable": sortable,
        "facetable": facetable
    }


    return field

'''

'''
def create_index(endpoint, headers, params, index_name):

    id_field = create_field(name="id", type="Edm.String", searchable="true", sortable="true", key="true")
    content_field = create_field(name="content", type="Edm.String", searchable="true")
    language_code_field = create_field(name="languageCode", type="Edm.String", searchable="true", filterable="true")
    key_phrases_field = create_field(name="keyPhrases", type="Collection(Edm.String)",  searchable="true")

    #metadata 
    metadata_author_field = create_field(name="authors", type="Edm.String", searchable="true")
    metadata_title_field = create_field(name="title", type="Edm.String", searchable="true", sortable="true")
    metadata_creation_date_field = create_field(name="creationDate", type="Edm.String", sortable="true", filterable="true")

    metadata_storage_name = create_field(name="storageName", type="Edm.String", searchable="true", sortable="true")
    metadata_storage_size = create_field(name="storageSize", type="Edm.Int64", sortable="true", filterable="true")

    fields_list = [id_field, content_field, language_code_field, key_phrases_field, metadata_author_field, metadata_title_field, metadata_creation_date_field, metadata_storage_name, metadata_storage_size]


    index_payload = {
        "name": index_name,
        "fields": fields_list
    }

    r = requests.put(endpoint + "/indexes/" + index_name, 
                    data=json.dumps(index_payload), headers=headers, params=params)
    print("creating index")

    print(r.status_code)



def create_indexer(endpoint, headers, params, indexer_name, datasource_name, index_name, skillset_name):
    indexer_payload = {
        "name": indexer_name,
        "description": None,
        "dataSourceName": datasource_name,
        "targetIndexName": index_name,
        "skillsetName": skillset_name,
        "fieldMappings": [
            {
                "sourceFieldName": "metadata_storage_path",
                "targetFieldName": "id",
                "mappingFunction":
                {"name": "base64Encode"}
            },
            {
                "sourceFieldName": "content",
                "targetFieldName": "content"
            }, 
            {
                "sourceFieldName": "metadata_storage_size",
                "targetFieldName": "storageSize"
            }, 
            {
                "sourceFieldName": "metadata_storage_name",
                "targetFieldName": "storageName"
            }, 
            {
                "sourceFieldName": "metadata_title", 
                "targetFieldName": "title"
            }, 
            {
                "sourceFieldName": "metadata_creation_date",
                "targetFieldName": "creationDate"   # doesn't ~always~ work
            },
            {
                "sourceFieldName": "metadata_author",
                "targetFieldName": "authors"        # doesn't work well. It depends how the authors are separated in the metadata
            }
        ],
        "outputFieldMappings":
        [
            {
                "sourceFieldName": "/document/pages/*/keyPhrases/*",
                "targetFieldName": "keyPhrases"
            },
            {
                "sourceFieldName": "/document/languageCode",
                "targetFieldName": "languageCode"
            }
        ],
        "parameters":
        {
            "maxFailedItems": -1, #ignore errors during data import
            "maxFailedItemsPerBatch": -1,
            "configuration":
            {
                "dataToExtract": "contentAndMetadata"
            }
        }
    }

    r = requests.put(endpoint + "/indexers/" + indexer_name,
                    data=json.dumps(indexer_payload), headers=headers, params=params)

    print("creating indexer")

    print(r.status_code)


'''

'''
# special skill
def extract_section(content, section_to_be_extracted):

   #select certain article
   article = content 
   
   section_req = {"section":section_to_be_extracted}

   # add the section name to the existing json so we can send it via the request
   article.update(section_req)
   req = json.dumps(article, indent=1)

   #print(article)

   section_extraction_url = os.getenv('SECTION_EXTRACTION_FUNCTION')
   #section_extraction_url = "http://localhost:7071/api/section_identifier"

   res = requests.get(section_extraction_url, data=req)

   print("extracting section")

   if section_to_be_extracted == "All":
      section_to_be_extracted = "Introduction"
      
   section_lowerletter = section_to_be_extracted.lower()
   section = res.json()[section_lowerletter][0]

   #save file for further use without having to run the services again
   #save_file('texts/article_' + str(article_index), section_lowerletter + '.txt', section)

   return section