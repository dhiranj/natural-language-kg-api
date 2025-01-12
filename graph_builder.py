import networkx as nx
from collections import defaultdict
import pandas as pd

def build_graph_with_name_mapping(datasets):
    graph = nx.DiGraph()  # Change to directed graph
    name_to_id = {}  # Dictionary to store name-to-ID mapping

    # Add nodes for scientists
    for _, row in datasets['top_1000_scientists'].iterrows():
        author_id = row['author_id']
        name = row['author_name']
        graph.add_node(author_id, name=name, rank=row['rank'],
                       total_citations=row['total_citations'], publication_count=row['publication_count'])
        name_to_id[name] = author_id

    # Add coauthor relationships (assumed undirected)
    for _, row in datasets['coauthor_mapping'].iterrows():
        author1, author2 = row['author_id_1'], row['author_id_2']
        if author1 in graph and author2 in graph:
            if not graph.has_edge(author1, author2):
                graph.add_edge(author1, author2, relationships=set())  # Initialize relationships as a set
                graph.add_edge(author2, author1, relationships=set())  # Ensure bidirectional edges
            graph[author1][author2]['relationships'].add('coauthor')
            graph[author2][author1]['relationships'].add('coauthor')

    # Add student-of relationships (directed from teacher to student)
    for _, row in datasets['teacher_student'].iterrows():
        teacher, student = row['teacher_id'], row['student_id']
        if teacher in graph and student in graph:
            if not graph.has_edge(teacher, student):
                graph.add_edge(teacher, student, relationships=set())
            graph[teacher][student]['relationships'].add('student-of')

    # Add same-college relationships (assumed undirected)
    same_college_data = datasets['same_college_mapping']
    for _, row in same_college_data.iterrows():
        if row['same_college_flag']:
            author1, author2 = row['author1_id'], row['author2_id']
            if graph.has_node(author1) and graph.has_node(author2):
                # Add edges if they don't already exist
                if not graph.has_edge(author1, author2):
                    graph.add_edge(author1, author2, relationships=set())
                graph[author1][author2]['relationships'].add('same-college')
                
                # For undirected behavior in DiGraph, add reverse edge
                if not graph.has_edge(author2, author1):
                    graph.add_edge(author2, author1, relationships=set())
                graph[author2][author1]['relationships'].add('same-college')


    return graph, name_to_id
