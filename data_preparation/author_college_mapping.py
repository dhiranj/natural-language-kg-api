import csv
import pandas as pd

# Input and output file paths
input_file = 'output.csv'  # Update this path as needed
output_file = 'author_college_mapping.csv'  # Output file path

# Step 1: Process the input file line by line to create author-college mapping
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['author_id', 'author_name', 'author_org']  # Define the required output fields
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header to the output CSV

    for row in reader:
        # Split the author_id, author_name, and author_org columns
        author_ids = row['author_id'].split(';') if row['author_id'] else []
        author_names = row['author_name'].split(';') if row['author_name'] else []
        author_orgs = row['author_org'].split(';') if row['author_org'] else []

        # Ensure the lengths of IDs, names, and orgs match
        if len(author_ids) == len(author_names) == len(author_orgs):
            for author_id, author_name, author_org in zip(author_ids, author_names, author_orgs):
                writer.writerow({
                    'author_id': author_id,
                    'author_name': author_name,
                    'author_org': author_org
                })

# Step 2: Remove duplicates from the output file and resave
# Load the written file into pandas
college_mapping_df = pd.read_csv(output_file)

# Remove duplicates
college_mapping_df = college_mapping_df.drop_duplicates()

# Save back to the same file
college_mapping_df.to_csv(output_file, index=False)

print(f"Author-college mapping has been processed, duplicates removed, and saved to '{output_file}'.")
