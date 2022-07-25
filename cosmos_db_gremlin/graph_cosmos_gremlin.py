from .graph_helper import populate_graph
from .graph_handler import cleanup_graph_query, query_graph

import os 
import subprocess

import sys
import time

PATH_TO_PWS_SCRIPTS = "C:\\Users\\danan\\Desktop\\School\\Bachelor's thesis\\public_github\\Thesis_Knowledge_Mining_Scientific_Articles\\cosmos_db_gremlin\\powershell_scripts"


'''
Create graphs in CosmosDB via background processes
'''
def powershell_create_graphs(graph_count):

    for index in range(graph_count):
        graph_name = "art_" + str(index)
        # run powershell script
        subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', PATH_TO_PWS_SCRIPTS + '\\create_container.ps1','-graphName' , "test"])

'''
Delete graphs via background processes
'''
def powershell_delete_graphs(graph_count):

    for index in range(graph_count):
        graph_name = 'art_'+ str(index)
        # run powershell script
        subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', PATH_TO_PWS_SCRIPTS + '\\delete_container.ps1','-graphName' , graph_name])
        