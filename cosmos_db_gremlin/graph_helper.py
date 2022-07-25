from pyparsing import empty
from .graph_handler import *
import re

'''
Populate an existing graph with the results from the Text Analytics
'''
def populate_graph(docs, graph_name):
    
    for entity_index, doc in enumerate(docs):
        # usually 1 entity is a vertex. The list below is the vertices connected via an edge (the relation). Exceptions below
        entities = [("", ""), ("", "")]
        vertex_edge_vertex_list_back = [(9999, 9999, 9999) for i in range(10)]

        relation_count = -1
        (initial_entity_1, initial_relation, initial_entity_2) = (None, None, None)

        for relation in doc.entity_relations:
            # we're keeping track only of the last 10 relations (so we can solve the exceptions)
            relation_count = relation_count + 1
            i = relation_count % 10

            # e.g. ValueOfExamination
            relation_type = relation.relation_type
    
            entity_index = 0        
            for role in relation.roles:
                # role.name e.g. Condition
                # role.entity.text e.g. covid
                entities[entity_index] = (role.name, role.entity.text)
                
                # exception
                # find edge between 2 existing vertices
                if (relation_type == "ValueOfExamination" or relation_type == "UnitOfExamination" or relation_type == "UnitOfCondition") and entity_index == 0 and is_number(entities[1][1]):
                    (initial_entity_1, initial_relation, initial_entity_2) = find_vertex_edge(entities[entity_index][1], vertex_edge_vertex_list_back)
                                        
                # exception
                # instead of a new vertex, add attribute to the found edge
                if (relation_type == "ValueOfExamination" or relation_type == "UnitOfExamination" or relation_type == "UnitOfCondition") and entity_index == 1 and (initial_relation != 9999 or initial_relation != None) and is_number(entities[1][1]):
                    query_graph(graph_name, "update", update_edge_query(str(initial_entity_1), str(initial_relation), str(initial_entity_2), entities[entity_index]))
                    #print("updated " + entity_1 + " -> " + rel + " -> " + entity_2+ "\t with " + str(entities[idx][0]) + " and " + str(entities[idx][1]))

                entity_index = entity_index + 1

            # don't create vertices for the exceptions
            if (relation_type == "ValueOfExamination" or relation_type == "UnitOfExamination" or relation_type == "UnitOfCondition") and is_number(entities[1][1]):
                continue

            if relation_type == "Abbreviation":
                continue

            # create vertices for each vertex (entities[0] and entities[1])
            query_graph(graph_name, "insert vertex", create_vertex_query(str(entities[0][0]), str(entities[0][1])))
            query_graph(graph_name, "insert vertex", create_vertex_query(str(entities[1][0]), str(entities[1][1])))
            
            # I didn't like the order for this one, so I switched the direction of the edge
            if relation_type == "QualifierOfCondition":
                query_graph(graph_name, "insert edge", create_edge_query(str(entities[0][1]), relation_type, str(entities[1][1])))
            else:
                query_graph(graph_name, "insert edge", create_edge_query(str(entities[1][1]), relation_type, str(entities[0][1])))
            
            # populate that we use to keep track of the previous relations
            vertex_edge_vertex_list_back[i] = (entities[1][1], relation_type, entities[0][1])
            #print("add to list:\n\t " + entities[1][1] + " -> " + relation_type + " -> " + entities[0][1])


'''
Find edge between 2 existing vertices
'''
def find_vertex_edge(entity, list):
    for e in reversed(list):
        if e[0] == entity:
            return e        
    return (9999, 9999, 9999)

'''
Verifies if string is number
'''
def is_number(string):

    if string.isnumeric():
        return True

    if bool(re.match("^\d+$", '123.21331')):
        return True

    if bool(re.match("^\d+?\.\d+?$", string)):
        return True

    return False