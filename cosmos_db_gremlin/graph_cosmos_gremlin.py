from .graph_helper import populate_graph
from .graph_handler import cleanup_graph_query, query_graph

import os 
import subprocess

import sys
import time

#query_graph("drop graph", cleanup_graph_query())
#query_graph("insert vertex", create_vertex_query("illness", "flu"))
#query_graph("insert edge", create_edge_query("covid-19", "bad", "flu"))
#query_graph("count vertices", count_vertices_query())

PATH_TO_PWS_SCRIPTS = "C:\\Users\\danan\\Desktop\\School\\Bachelor's thesis\\code\\thesis_code\\cosmos_db_gremlin\\powershell_scripts"

'''

'''
def create_graph(docs, graph_name):

    #Query_graph(graph_name, "cleanup", cleanup_graph_query())    

    populate_graph(docs, graph_name)

    print("\nAnd that's all for this part!")

'''

python -c "from graph_cosmos_gremlin import powershell_create_graphs; powershell_create_graphs(10)"

'''
def powershell_create_graphs(graph_count):

    for index in range(graph_count):
        graph_name = "art_" + str(index)
        # run powershell script
        subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', PATH_TO_PWS_SCRIPTS + '\\create_container.ps1','-graphName' , "test"])
        #time.sleep(10)

def print_hello():
    print("hello")

'''

'''
def powershell_delete_graphs(graph_count):

    for index in range(graph_count):
        graph_name = 'art_'+ str(index)
        # run powershell script
        subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Unrestricted', '-File', PATH_TO_PWS_SCRIPTS + '\\delete_container.ps1','-graphName' , graph_name])
        