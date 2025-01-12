import pandas as pd

# # Load the data
sample_output_file_path = 'output.csv'  # Update this path as needed
sample_output_df = pd.read_csv(sample_output_file_path)

coauthor_data = sample_output_df[['id', 'author_id']].copy()
coauthor_data['author_id'] = coauthor_data['author_id'].str.split(';')
coauthor_data = coauthor_data.explode('author_id')

coauthor_pairs = coauthor_data.merge(coauthor_data, on='id', suffixes=('_1', '_2'))
coauthor_pairs = coauthor_pairs[coauthor_pairs['author_id_1'] != coauthor_pairs['author_id_2']].drop_duplicates()

# Save coauthor pairs
coauthor_pairs.to_csv("coauthor_pairs.csv", index=False)