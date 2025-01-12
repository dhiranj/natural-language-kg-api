# Knowledge Graph Dataset Preparation

## Step 1: Obtain the Dataset

- **Source**: [CSV Conversion - All Fields](https://www.kaggle.com/code/shreyasbhatk/csv-conversion-all-fields/input)
- Download the JSON dataset (e.g., `dblp.v12.json`).

## Step 2: Convert JSON to CSV

- Use `json_to_csv.py` to extract and preprocess fields like:
  - `id`, `title`, `author_name`, `author_id`, `n_citation`, `references`, and `venue_name`.
- Script processes JSON into `output.csv`.

## Step 3: Generate Top 1,000 Authors Dataset
- Use  `top_1k_scientist.py`
- Load the subset data and group by author to aggregate `total_citations` and `publication_count`.
- Rank authors based on citations and publications.
- Extract the top 1,000 authors and save to `top_1000_computer_scientists.csv`.

## Step 4: Generate Author-College Mapping

- **Code File**: `author_college_mapping.py`
- Process the dataset to extract `author_id`, `author_name`, and `author_org`.
- Create a mapping of authors to their associated colleges or organizations.
- Remove duplicates to ensure clean data.
- Save the mapping to `author_college_mapping.csv`.

## Step 5: Filter Author-College Mapping for Top 1,000 Authors

- **Code File**: `filtered_author_college_mapping.py`
- Load the `author_college_mapping.csv` and `top_1000_computer_scientists.csv` datasets.
- Filter the author-college mapping to include only the top 1,000 authors.
- Save the filtered mapping to `filtered_author_college_mapping.csv`.

## Step 6: Compute Same-College Relationships

- **Code File**: `same_college.py`
- Load the `filtered_author_college_mapping.csv` dataset.
- Identify pairs of authors who attended the same college based on the `author_org` field.
- Generate a new dataset with columns:
  - `author1_id`, `author2_id`, `author1_org`, `author2_org`, and `same_college_flag`.
- Save the results to `same_college_results.csv`.

## Step 7: Generate Author Mapping

- **Code File**: `author_mapping.py`
- Load the `output.csv` dataset.
- Extract `author_id` and `author_name` to create a mapping.
- Remove duplicates to ensure clean data.
- Save the mapping to `author_mapping.csv`.

## Step 8: Filter Author Mapping for Top 1,000 Authors

- **Code File**: `filtered_author_mapping.py`
- Load the `author_mapping.csv` and `top_1000_computer_scientists.csv` datasets.
- Filter the author mapping to include only authors in the top 1,000.
- Save the filtered mapping to `filtered_author_mapping.csv`.

## Step 9: Generate Coauthor Pairs

- **Code File**: `coauthor_pairs.py`
- Load the `output.csv` dataset.
- Extract and process `author_id` to identify coauthor relationships.
- Generate pairs of coauthors for each paper.
- Save the coauthor pairs to `coauthor_pairs.csv`.

## Step 10: Filter Coauthor Data

- **Code File**: `filtered_coauthor.py`
- Load the `coauthor_pairs.csv` and `top_1000_computer_scientists.csv` datasets.
- Filter coauthor relationships to include only pairs where at least one author is in the top 1,000.
- Save the filtered data to `filtered_coauthor_mapping.csv`.

## Step 11: Filter Coauthor Mapping for Top 1,000 Authors

- **Code File**: `filtered_coauthor_mapping_top_1000.py`
- Load the `filtered_coauthor_mapping.csv` and `top_1000_computer_scientists.csv` datasets.
- Filter coauthor relationships to include only pairs where both authors are in the top 1,000.
- Save the filtered coauthor mapping to `filtered_coauthor_mapping_top_1000.csv`.

## Step 12: Create ID to Author Mapping for Top 1,000 Authors

- **Code File**: `id_to_author_mapping.py`
- Load the `output.csv` and `top_1000_computer_scientists.csv` datasets.
- Extract paper IDs and author IDs, retaining only author IDs that belong to the top 1,000 authors.
- Save the mapping to `id_to_author_mapping.csv`.


## Step 13: Generate Teacher-Student Relationships

- **Code File**: `teacher_student.py`
- Load the `top_1000_computer_scientists.csv` dataset.
- Divide the dataset into hierarchical levels (e.g., teachers, students, and students of students).
- Create teacher-student relationships for each level.
- Save the relationships to `teacher_student.csv`.
