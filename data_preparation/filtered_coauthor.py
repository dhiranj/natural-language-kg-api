import pandas as pd

# Load the co-author mapping and top 1000 scientists data
coauthor_file_path = 'coauthor_pairs.csv'  # Update with the correct file path
top_1000_file_path = 'top_1000_computer_scientists.csv'  # Update with the correct file path

# Read the datasets
coauthor_data = pd.read_csv(coauthor_file_path)
top_1000_data = pd.read_csv(top_1000_file_path)

# Extract the list of author IDs from the top 1000 scientists dataset
top_1000_author_ids = set(top_1000_data['author_id'])

# Filter coauthor data to keep only records where both author_id_1 and author_id_2 are in the top 1000 author IDs
filtered_coauthor_data = coauthor_data[
    (coauthor_data['author_id_1'].isin(top_1000_author_ids))
]

# Save the filtered data to a new file
filtered_coauthor_file_path = 'filtered_coauthor_mapping.csv'  # Update with your desired file name
filtered_coauthor_data.to_csv(filtered_coauthor_file_path, index=False)

print(f"The filtered coauthor mapping data has been saved to '{filtered_coauthor_file_path}'.")
