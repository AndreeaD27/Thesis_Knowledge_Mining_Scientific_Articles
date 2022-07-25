import os
from re import L
from unittest import result
from dotenv import load_dotenv
import os
from pprint import pprint # pretty printer
import requests

from cognitive_search_components import *
from language_analytics_health import *
from article import *
from cognitive_search_helper import *

'''

'''
def main():

    load_dotenv()
    
    # Define the names for the data source, skillset, index and indexer
    datasource_name = "cogsrch-py-datasource"
    skillset_name = "cogsrch-py-skillset"
    index_name = "cogsrch-py-index"
    indexer_name = "cogsrch-py-indexer"

    endpoint = os.getenv('SEARCH_ENDPOINT')
    admin_key = os.getenv('SEARCH_ADMIN_API_KEY')

    headers = {
        'Content-Type':'application/json',
        'api-key': admin_key
    }

    params = {
        'api-version':'2020-06-30'
    }

    # optional
    '''       
    clear_previous_resources(endpoint, headers, params, datasource_name, skillset_name, index_name, indexer_name)

    create_datasource(endpoint, headers, params, datasource_name)
    print("1")
    create_skillset(endpoint, headers, params, skillset_name)
    print("2")
    create_index(endpoint, headers, params, index_name)
    print("3")
    create_indexer(endpoint, headers, params, indexer_name, datasource_name, index_name, skillset_name)
    print("4")'''
    
    search_content(endpoint, headers, params, index_name)
    print("5")




if __name__ == "__main__":
    main()