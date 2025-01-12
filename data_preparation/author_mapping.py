import csv
import pandas as pd

# Step 1: Generate the author mapping and write to file
input_file = 'output.csv'  # Input file path
output_file = 'author_mapping.csv'  # Output file path

# Process the input file line by line to create author mapping
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['author_id', 'author_name']  # Define the required output fields
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header to the output CSV

    for row in reader:
        # Split the author_id and author_name columns
        author_ids = row['author_id'].split(';') if row['author_id'] else []
        author_names = row['author_name'].split(';') if row['author_name'] else []

        # Ensure the lengths of IDs and names match
        if len(author_ids) == len(author_names):
            for author_id, author_name in zip(author_ids, author_names):
                writer.writerow({'author_id': author_id, 'author_name': author_name})

# Step 2: Remove duplicates from the output file and resave
# Load the written file into pandas
author_mapping_df = pd.read_csv(output_file)

# Remove duplicates
author_mapping_df = author_mapping_df.drop_duplicates()

# Save back to the same file
author_mapping_df.to_csv(output_file, index=False)

print(f"Author mapping has been processed, duplicates removed, and saved to '{output_file}'.")
