import pandas as pd

# File paths
author_college_mapping_file = 'author_college_mapping.csv'  # Path to the author-college mapping dataset
top_1000_file = 'top_1000_computer_scientists.csv'  # Path to the top 1000 dataset
filtered_author_college_file = 'filtered_author_college_mapping.csv'  # Output file path

# Load the datasets
author_college_mapping = pd.read_csv(author_college_mapping_file)
top_1000 = pd.read_csv(top_1000_file)

# Extract the list of author IDs from the top 1000 dataset
top_1000_author_ids = set(top_1000['author_id'])

# Filter the author-college mapping dataset to keep only rows with author IDs in the top 1000
filtered_author_college_mapping = author_college_mapping[author_college_mapping['author_id'].isin(top_1000_author_ids)]

# Save the filtered dataset
filtered_author_college_mapping.to_csv(filtered_author_college_file, index=False)

print(f"Filtered author-college mapping has been saved to '{filtered_author_college_file}'.")
