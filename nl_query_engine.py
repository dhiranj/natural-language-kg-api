import openai
import networkx as nx
import ast
import os

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_query_code(natural_language_query):
    """
    Generate Python code for a natural language query using OpenAI GPT.

    Args:
        natural_language_query (str): The user input query in natural language.

    Returns:
        str: Generated Python code.
    """
    # Create the prompt
    prompt = f"""
                You are an assistant that converts natural language queries into Python code for querying a NetworkX graph.
                The graph contains nodes representing scientists, and edges represent relationships between them. 
                Each node has the following attributes:
                - `name`: The scientist's name.
                - `rank`: The scientist's rank in the top 1000.
                - `total_citations`: The total number of citations the scientist has received.
                - `publication_count`: The total number of publications by the scientist.

                The graph supports the following relationships:
                - `coauthor`: Two scientists have coauthored a paper.
                - `student-of`: One scientist was a PhD student of another scientist.
                - `same-college`: Two scientists are from the same college/university.

                Example:
                Input: "List all the coauthors of Alice who were in the same university as Alice."
                Output:
                ```python
                def query(graph, name_to_id):
                    author_id = name_to_id.get("Alice")
                    if not author_id:
                        return []
                    coauthors = [n for n in graph.neighbors(author_id) if 'coauthor' in graph[author_id][n]['relationships']]
                    same_college = [n for n in graph.neighbors(author_id) if 'same-college' in graph[author_id][n]['relationships']]
                    result = set(coauthors).intersection(same_college)
                    return [graph.nodes[n]['name'] for n in result]

                result = query(graph, name_to_id)

    Input: "{natural_language_query}"
    Output:
    """

    # Call the ChatCompletion API
    response = openai.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an assistant that converts natural language queries into Python code."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
        max_tokens=300,
        temperature=0.0
    )

    # Extract the generated Python code
    return response.choices[0].message.content.strip()

def is_safe_code(code):
    """
    Check the safety of the Python code to prevent execution of harmful code.

    Args:
        code (str): The Python code to validate.

    Returns:
        bool: True if the code is safe, False otherwise.
    """
    try:
        # Parse the code into an Abstract Syntax Tree (AST)
        tree = ast.parse(code, mode="exec")

        # Traverse the AST and check for potentially dangerous nodes
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # Disallow imports
                return False
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                # Disallow exec(), eval(), os.system(), etc.
                if node.func.id in {"exec", "eval", "os.system", "subprocess", "open"}:
                    return False
            elif isinstance(node, ast.Attribute) and node.attr in {"system", "popen"}:
                # Disallow system-related calls
                return False

        # If no dangerous constructs are found, the code is safe
        return True
    except Exception as e:
        print(f"Error during code safety check: {e}")
        return False

def execute_query_code(code, graph, name_to_id):
    """
    Execute the generated Python code safely.

    Args:
        code (str): The generated Python code as a string.
        graph (networkx.Graph): The knowledge graph.
        name_to_id (dict): Mapping from names to author IDs.

    Returns:
        Any: The result of executing the code.
    """
    # Clean the code by removing Markdown-style code block delimiters
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    if code.endswith("```"):
        code = code[:-len("```")].strip()

    # Check the code for safety
    if not is_safe_code(code):
        return {
            "error": "The generated code contains unsafe or disallowed operations.",
            "code": code
        }

    # Prepare the local namespace for execution
    local_namespace = {"graph": graph, "name_to_id": name_to_id, "result": None}
    try:
        # Execute the code
        exec(code, {}, local_namespace)
        return local_namespace.get("result", "No result returned by the query.")
    except Exception as e:
        return {"error": str(e), "code": code}

