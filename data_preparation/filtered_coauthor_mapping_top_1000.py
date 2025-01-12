import pandas as pd

# Load the datasets
top_1000_scientists_path = "top_1000_computer_scientists.csv"  # Replace with the correct file path
coauthor_mapping_path = "filtered_coauthor_mapping.csv"  # Replace with the correct file path

top_1000_scientists = pd.read_csv(top_1000_scientists_path)
coauthor_mapping = pd.read_csv(coauthor_mapping_path)

# Filter out records where either author1 or author2 is not in the top 1000 scientists
top_1000_ids = set(top_1000_scientists['author_id'])

filtered_coauthor_mapping = coauthor_mapping[
    (coauthor_mapping['author_id_1'].isin(top_1000_ids)) &
    (coauthor_mapping['author_id_2'].isin(top_1000_ids))
]

# Save the filtered coauthor mapping to a new file
output_path = "filtered_coauthor_mapping_top_1000.csv"  # Replace with your desired output path
filtered_coauthor_mapping.to_csv(output_path, index=False)

# Display a sample of the filtered data
print(filtered_coauthor_mapping.head())
