def get_author_id_by_name(name_to_id, name):
    """Retrieve author ID by name using precomputed dictionary."""
    return name_to_id.get(name, None)

def coauthors_same_university(graph, name_to_id, author_name):
    """
    Find coauthors of a given author who are from the same university, using the "same-college" relationship.

    Args:
        graph (networkx.DiGraph): The graph containing authors and their relationships.
        name_to_id (dict): Mapping from author names to their IDs.
        author_name (str): The name of the author to search for.

    Returns:
        list: A list of author names who are coauthors and belong to the same university.
    """
    # Get the author ID for the given name
    author_id = name_to_id.get(author_name)
    if not author_id:
        return []

    # Find neighbors with the "same-college" relationship
    same_college_neighbors = [
        neighbor for neighbor in graph.successors(author_id)  # Use successors for directed relationships
        if 'same-college' in graph[author_id][neighbor].get('relationships', set())
    ]

    # Return their names
    return [graph.nodes[neighbor]['name'] for neighbor in same_college_neighbors]

def did_write_paper_together(graph, name_to_id, author1_name, author2_name):
    """
    Check if two authors wrote a paper together (are coauthors).
    """
    # Get author IDs
    author1_id = get_author_id_by_name(name_to_id, author1_name)
    author2_id = get_author_id_by_name(name_to_id, author2_name)

    # If either ID is missing, return False
    if not author1_id or not author2_id:
        return False

    # Check for 'coauthor' relationship
    return graph.has_edge(author1_id, author2_id) and 'coauthor' in graph[author1_id][author2_id].get('relationships', set())

def scientists_with_students_students(graph):
    """
    Find scientists who have students whose students are also coauthors with the original scientist.
    """
    result = []
    for node in graph.nodes:
        # Get direct students
        students = [
            neighbor for neighbor in graph.successors(node)  # Use successors for "student-of"
            if 'student-of' in graph[node][neighbor].get('relationships', set())
        ]

        # Check students of students
        for student in students:
            students_of_students = [
                neighbor for neighbor in graph.successors(student)  # Use successors for "student-of"
                if 'student-of' in graph[student][neighbor].get('relationships', set())
            ]

            # Check if any of the student's students are coauthors with the original scientist
            if any(
                graph.has_edge(node, sos) and 'coauthor' in graph[node][sos].get('relationships', set())
                for sos in students_of_students
            ):
                result.append(graph.nodes[node]['name'])
                break  # Avoid duplicates in the result

    return result
