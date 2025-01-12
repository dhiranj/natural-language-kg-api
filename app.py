from fastapi import FastAPI, Query, Body, HTTPException
from urllib.parse import unquote
from data_loader import load_datasets
from graph_builder import build_graph_with_name_mapping
from query_engine import coauthors_same_university, did_write_paper_together, scientists_with_students_students
from nl_query_engine import generate_query_code, execute_query_code

app = FastAPI()

# Load datasets and build the graph on server startup
datasets = load_datasets()
knowledge_graph, name_to_id = build_graph_with_name_mapping(datasets)

@app.get("/coauthors-same-university")
def coauthors_same_university_api(author_name: str):
    """
    API endpoint to retrieve coauthors of an author who are from the same university.
    """
    try:
        if not author_name:
            raise HTTPException(status_code=400, detail="Author name is required.")
        result = coauthors_same_university(knowledge_graph, name_to_id, author_name)
        return {"author_name": author_name, "coauthors_same_university": result}
    except KeyError:
        raise HTTPException(status_code=404, detail="Author not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/did-write-paper")
def did_write_paper_api(author1: str, author2: str):
    """
    API endpoint to check if two authors wrote a paper together.
    """
    try:
        if not author1 or not author2:
            raise HTTPException(status_code=400, detail="Both author1 and author2 are required.")
        result = did_write_paper_together(knowledge_graph, name_to_id, author1, author2)
        return {"author1": author1, "author2": author2, "did_write_paper": result}
    except KeyError:
        raise HTTPException(status_code=404, detail="One or both authors not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/scientists-with-students-students")
def scientists_with_students_students_api():
    """
    API endpoint to retrieve scientists who have students whose students are coauthors.
    """
    try:
        result = scientists_with_students_students(knowledge_graph)
        return {"scientists_with_students_students": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/nl-query")
def nl_query_api(query: str = Body(..., embed=True)):
    """
    Handle natural language queries to the knowledge graph.

    Args:
        query (str): Natural language query.

    Returns:
        dict: Results from executing the query.
    """
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query is required.")
        
        # Generate Python code for the query
        generated_code = generate_query_code(query)

        # Execute the code
        result = execute_query_code(generated_code, knowledge_graph, name_to_id)

        return {
            "query": query,
            "generated_code": generated_code,
            "result": result
        }
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Error in generated code syntax.")
    except KeyError:
        raise HTTPException(status_code=404, detail="Entity not found in the knowledge graph.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
