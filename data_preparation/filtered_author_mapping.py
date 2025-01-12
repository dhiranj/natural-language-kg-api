import pandas as pd

# File paths
author_mapping_file = 'author_mapping.csv'  # Update with the correct path to the full author mapping dataset
top_1000_file = 'top_1000_computer_scientists.csv'  # Update with the correct path to the top 1000 dataset
filtered_author_mapping_file = 'filtered_author_mapping.csv'  # Output file path

# Load the datasets
author_mapping = pd.read_csv(author_mapping_file)
top_1000 = pd.read_csv(top_1000_file)

# Extract the author IDs from the top 1000 dataset
top_1000_author_ids = set(top_1000['author_id'])

# Filter the author mapping dataset to keep only rows with author IDs in the top 1000
filtered_author_mapping = author_mapping[author_mapping['author_id'].isin(top_1000_author_ids)]

# Save the filtered dataset
filtered_author_mapping.to_csv(filtered_author_mapping_file, index=False)

print(f"Filtered author mapping has been saved to '{filtered_author_mapping_file}'.")
