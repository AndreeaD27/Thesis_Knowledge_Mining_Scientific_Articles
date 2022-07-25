from gremlin_python.driver import client, serializer, protocol
from gremlin_python.driver.protocol import GremlinServerError

import os
import traceback
import sys

import asyncio

from dotenv import load_dotenv

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


load_dotenv()

cosmos_endpoint = os.getenv('COSMOS_SERVICE_NAME')
cosmos_admin_key = os.getenv('COSMOS_ADMIN_KEY')
database_name = os.getenv('COSMOS_DATABASE_NAME')
#graph_name = os.getenv('COSMOS_GRAPH_NAME')

'''
cosmos_endpoint = os.getenv('TEST_COSMOS_SERVICE_NAME')
cosmos_admin_key = os.getenv('TEST_COSMOS_ADMIN_KEY')
database_name = os.getenv('TEST_COSMOS_DATABASE_NAME')
graph_name = os.getenv('TEST_COSMOS_GRAPH_NAME')
'''

'''

'''
def query_graph(graph_name, query_type, query):

    try:
        cosmos_client = client.Client('wss://'+cosmos_endpoint+'.gremlin.cosmos.azure.com:443/', 'g',
                            username="/dbs/"+database_name+"/colls/"+graph_name,
                            password=cosmos_admin_key,
                            message_serializer=serializer.GraphSONSerializersV2d0()
                            )

        #print("Welcome to Azure Cosmos DB + Gremlin on Python!")

        if query_type == "cleanup":
            # Drop the entire Graph
            cleanup_graph(cosmos_client, query)

        elif query_type == "insert vertex":
            # Insert all vertices
            insert_vertices(cosmos_client, query)

        elif query_type == "insert edge":
            # Create edges between vertices
            insert_edges(cosmos_client, query)

        elif query_type == "update":
            # Update a vertex
            update(cosmos_client, query)

        elif query_type == "count vertices":
            # Count all vertices
            count_vertices(cosmos_client, query)

        elif query_type == "execute traversal":
            # Execute traversals and get results
            execute_traversals(cosmos_client, query)

        elif query_type == "drop vertex" or query_type == "drop edge":
            # Drop a few vertices and edges
            execute_drop_operations(cosmos_client, query)

        elif query_type == "test":
            test(cosmos_client, query)

    except GremlinServerError as e:
        print('Code: {0}, Attributes: {1}'.format(e.status_code, e.status_attributes))

        # GremlinServerError.status_code returns the Gremlin protocol status code
        # These are broad status codes which can cover various scenaios, so for more specific
        # error handling we recommend using GremlinServerError.status_attributes['x-ms-status-code']
        # 
        # Below shows how to capture the Cosmos DB specific status code and perform specific error handling.
        # See detailed set status codes than can be returned here: https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#status-codes
        #
        # See also list of available response status attributes that Gremlin API can return:
        #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
        cosmos_status_code = e.status_attributes["x-ms-status-code"]
        if cosmos_status_code == 409:
            print('Conflict error!')
        elif cosmos_status_code == 412:
            print('Precondition error!')
        elif cosmos_status_code == 429:
            print('Throttling error!');
        elif cosmos_status_code == 1009:
            print('Request timeout error!')
        else:
            print("Default error handling")

        traceback.print_exc(file=sys.stdout) 
        sys.exit(1)

'''

'''
def print_status_attributes(result):
    # random so I don't get errors
    a = 1
    # This logs the status attributes returned for successful requests.
    # See list of available response status attributes (headers) that Gremlin API can return:
    #     https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-headers#headers
    #
    # These responses includes total request units charged and total server latency time.
    # 
    # IMPORTANT: Make sure to consume ALL results returned by client to the final status attributes
    # for a request. Gremlin result are stream as a sequence of partial response messages
    # where the last response contents the complete status attributes set.
    #
    # This can be 
    #print("\tResponse status_attributes:\n\t{0}".format(result.status_attributes))

# NOTE: The below methods have A LOT of duplicate code. I'll let them like this just because they provide clarity in results in the terminal


'''

'''
# test method (runs any query)
def test(client, query_list):
    for query in query_list:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\t Result -> :\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))
        print("\n")
        print_status_attributes(callback.result())


# drop the whole graph 
def cleanup_graph(client, cleanup_query):
    print("\n> {0}".format(
        cleanup_query))
    callback = client.submitAsync(cleanup_query)
    if callback.result() is not None:
        callback.result().all().result() 
    print("\n")
    print_status_attributes(callback.result())

 # insert vertices
def insert_vertices(client, insert_vertices_query):
    for query in insert_vertices_query:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        '''if callback.result() is not None:
            print("\tInserted this vertex:\n\t{0}".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query: {0}".format(query))'''
        
        if callback.result() is None:
             print("Something went wrong with this query: {0}".format(query))
        print("\n")
        #print_status_attributes(callback.result())


'''

'''
# insert edges
def insert_edges(client, insert_edges_query):
    for query in insert_edges_query:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tInserted this edge:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))
        print_status_attributes(callback.result())

# update either a vertex or an edge
def update(client, update_query):
    for query in update_query:
        print("\n> {0}\n".format(query))
        callback = client.submitAsync(query)
        if callback.result() is not None:
            print("\tUpdated this:\n\t{0}\n".format(
                callback.result().all().result()))
        else:
            print("Something went wrong with this query:\n\t{0}".format(query))

        print_status_attributes(callback.result())


'''

'''
# count vertices
def count_vertices(client, count_vertices_query):
    print("\n> {0}".format(
        count_vertices_query))
    callback = client.submitAsync(count_vertices_query)
    if callback.result() is not None:
        print("\tCount of vertices: {0}".format(callback.result().all().result()))
    else:
        print("Something went wrong with this query: {0}".format(
            count_vertices_query))

    print("\n")
    print_status_attributes(callback.result())


'''

'''
# execute traversals
def execute_traversals(client, traversals_query):
    for key in traversals_query:
        print("{0}:".format(key))
        print("> {0}\n".format(
            traversals_query[key]))
        callback = client.submitAsync(traversals_query[key])
        for result in callback.result():
            print("\t{0}".format(str(result)))
        
        print("\n")
        print_status_attributes(callback.result())


'''

'''
# drop operations
def execute_drop_operations(client, drop_operations_query):
    for key in drop_operations_query:
        print("{0}:".format(key))
        print("\n> {0}".format(
            drop_operations_query[key]))
        callback = client.submitAsync(drop_operations_query[key])
        for result in callback.result():
            print(result)
        print_status_attributes(callback.result())


# NOTE: the below methods are for QUERY GENERATION in Gremlin

# type is the general type of vertex or edge (e.g. Condition or TimeOfCondition)
# id is specific for each vertex (e.g. covid)
# from_id is the vertex from which the edge leaves
# to_id is the vertex in which the edge enters
# property is a (key, value) pair


'''

'''
def create_vertex_query(type, id):
    return ["g.V().has('" + type + "','id','" + id + "').fold().coalesce(unfold(),addV('" + type + "').property('id','" + id + "').property('pk', 'pk'))"]


'''

'''
def create_edge_query(from_id, type, to_id, property = None):
    if property != None:
        return ["g.V('"+ from_id + "').addE('" + type + "').to(g.V('" + to_id + "')).property('" + str(property[0]) + "', '" + str(property[1]) +"')"]
    return ["g.V('"+ from_id + "').addE('" + type + "').to(g.V('" + to_id + "'))"]


'''

'''
def update_vertex_query(id, property):
    return ["g.V('" + id + "').property('" + str(property[0]) + "', '" + str(property[1]) +"')"]


'''

'''
def update_edge_query(from_id, edge_type, to_id, property):
    return ["g.V('" + from_id + "').outE('" + edge_type + "').where(inV().hasId('" + to_id + "')).property('" + str(property[0]) + "', '" + str(property[1]) +"')"]


'''

'''
def count_vertices_query():
    return "g.V().count()"


'''

'''
def cleanup_graph_query():
    return "g.V().drop()"



# testing purposes 

