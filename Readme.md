# **Natural Language Query System for a Knowledge Graph of Computer Scientists**

## **Task**

The goal is to create a relationship graph for the top 1000 computer scientists and allow querying on top of it. The knowledge graph supports the following relationships:

- **`student-of`**: One scientist was a PhD student of another.
- **`coauthor`**: Two scientists have coauthored a paper together.
- **`same-college`**: Two scientists are from the same college/university.

The system provides an interface to handle natural language queries, converting them into Python code to query the knowledge graph. Example queries include:

- "List all the coauthors of X who were in the same university as X."
- "Did X and Y write a paper together?"
- "List the scientists who have written a paper with a student of their students."

---

## **Solution Overview**

The solution consists of three main components:

1. **Knowledge Graph Construction**:
   - Built using `NetworkX`, representing nodes (scientists) and edges (relationships).

2. **Natural Language Query Processing**:
   - Uses OpenAI GPT models to convert user queries into Python code.

3. **Execution and Validation**:
   - Validates the generated code for safety and executes it against the knowledge graph to provide results.

---

## **Features**

- Converts natural language queries into Python code using OpenAI GPT models.
- Supports relationships like `coauthor`, `student-of`, and `same-college`.
- Validates and executes the generated Python code safely.
- RESTful API for querying the graph.

---

## **System Components**

### **1. Knowledge Graph**

The graph is built using the following datasets:
- **Top 1000 Computer Scientists**:
  Contains details like name, rank, total citations, and publication count.
- **Coauthor Relationships**:
  Indicates whether two scientists have coauthored a paper.
- **Student-Teacher Relationships**:
  Maps PhD advisors to their students.
- **Same College Relationships**:
  Identifies scientists from the same college/university.

To generate these datasets, refer to the **`KnowledGegraph.md`** file. This document outlines all the steps and scripts required to preprocess the raw data into usable datasets for constructing the knowledge graph.


### **2. API Endpoints**

#### `/coauthors-same-university`
Retrieve coauthors of a scientist who are from the same university.

#### `/did-write-paper`
Check if two scientists have coauthored a paper.

#### `/scientists-with-students-students`
List scientists who have written a paper with a student of their students.

#### `/nl-query`
Handle natural language queries, generate Python code, and execute it against the graph.


## How It Works

1. **Natural Language Input**: Users provide a natural language query (e.g., "Who are the coauthors of John Doe?").
2. **Code Generation**: The API uses OpenAI GPT models to generate Python code that can query the knowledge graph.
3. **Safety Validation**: The generated code is validated for safety using Python's `ast` module to prevent execution of unsafe or malicious code.
4. **Query Execution**: The validated code is executed against a NetworkX-based knowledge graph, and results are returned to the user.

## **How to Build and Run**

### **Prerequisites**
- Python 3.12
- `pip` package manager
- An OpenAI API key


1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/natural-language-kg-api.git
   cd natural-language-kg-api
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set OpenAI API Key: Add your OpenAI API key to the environment:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```
   On Windows:
   ```bash
   set OPENAI_API_KEY="your-openai-api-key"
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

5. Open the interactive API documentation in your browser:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Evaluation

To evaluate the system, consider the following criteria:

### Correctness
- Test various natural language queries and validate if the results are accurate.
- Examples:
  - "Did Alice and Bob coauthor a paper?"
  - "List all the coauthors of Qiang Yang who are from the same university as Qiang Yang."

### Code Quality
- Validate the generated Python code for correctness and safety.

### Comprehensiveness
- Assess the coverage of the graph relationships (e.g., coauthor, student-of, same-college).

### Performance
- Test the response time for complex queries on large datasets.

### Security
- Ensure no harmful code can be executed (e.g., `os.system` or `eval`).


## Future Improvements

### Add Caching for Repeated Queries
- Implement caching to store results of frequently requested queries for better performance.

### Fine-Tune OpenAI Models
- Train GPT models on more domain-specific data to improve the accuracy of the generated code.

### Support Additional Graph Query Types
- Add advanced operations such as:
  - Finding the shortest path between two scientists.
  - Identifying communities or clusters in the graph.
