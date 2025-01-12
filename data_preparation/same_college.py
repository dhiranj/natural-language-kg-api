import pandas as pd

# Load the dataset
file_path = 'filtered_author_college_mapping.csv'
author_data = pd.read_csv(file_path)

def compute_same_college(df):
    """
    Compute pairs of authors who went to the same college based on the `author_org`.

    Args:
    df (pd.DataFrame): Input DataFrame with `author_id`, `author_name`, and `author_org`.

    Returns:
    pd.DataFrame: DataFrame with columns `author1_id`, `author2_id`, `author1_org`, `author2_org`, and `same_college_flag`.
    """
    # Drop rows where `author_org` is NaN
    df = df.dropna(subset=['author_org']).reset_index(drop=True)

    # Create a dictionary mapping each college to a list of author IDs
    college_to_authors = {}
    for _, row in df.iterrows():
        college = row['author_org']
        author_id = row['author_id']
        if college not in college_to_authors:
            college_to_authors[college] = []
        college_to_authors[college].append(author_id)

    # Prepare results based on the dictionary
    results = []
    for college, authors in college_to_authors.items():
        if len(authors) > 1:  # If more than one author went to the same college
            for i, author1 in enumerate(authors):
                for author2 in authors[i + 1:]:  # Compare each pair within the list
                    results.append({
                        'author1_id': author1,
                        'author2_id': author2,
                        'author1_org': college,
                        'author2_org': college,
                        'same_college_flag': True
                    })

    return pd.DataFrame(results)

# Apply the function to compute pairs
same_college_results = compute_same_college(author_data)

# Save the results to a new CSV file
output_path = 'same_college_results.csv'
same_college_results.to_csv(output_path, index=False)

print(f"Results saved to: {output_path}")
