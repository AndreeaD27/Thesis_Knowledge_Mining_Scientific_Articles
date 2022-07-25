from graph_handler import *


query_graph("art_0", "insert vertex", create_vertex_query("illness", "malaria"))
#query_graph("insert vertex", create_vertex_query("cure", "vaccine"))

#query_graph("insert edge", create_edge_query("covid", "bad", "flu"))
#query_graph("insert edge", create_edge_query("covid", "efficient", "vaccine"))
#query_graph("insert edge", create_edge_query("flu", "efficient", "vaccine"))

# drop an edge
#query = ["g.V('covid').outE('bad').where(inV().hasId('flu')).drop()"]

# edit the labels of an edge
#query = ["g.V('covid').outE('efficient').where(inV().hasId('vaccine')).property('success', 32)"]

# get property of edge
#query = ["g.V().has('id','covid').outE('efficient').as('e').inV().has('id', 'vaccine').as('v').select('e','v').by(valueMap())"]

#query_graph("art_0", query)

#query_graph("count vertices", count_vertices_query())

#query_graph("cleanup", cleanup_graph_query())


print("\nAnd that's all! Sample complete")
