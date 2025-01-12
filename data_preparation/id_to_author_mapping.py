import csv

# File paths
input_file = 'output.csv'  # Path to the input file
top_1000_file = 'top_1000_computer_scientists.csv'  # Path to the top 1000 authors file
output_file = 'id_to_author_mapping.csv'  # Output file

# Load the top 1000 authors to get the valid author IDs
top_1000_authors = set()
with open(top_1000_file, 'r') as top_file:
    top_reader = csv.DictReader(top_file)
    for row in top_reader:
        top_1000_authors.add(row['author_id'])

# Read the input file line by line and create the mapping table
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['id', 'author_id']  # Define the output columns
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header to the output file

    for row in reader:
        # Extract the paper ID and author IDs
        paper_id = row['id']
        author_ids = row['author_id'].split(';') if row['author_id'] else []

        # Write only those author IDs that are in the top 1000 authors
        for author_id in author_ids:
            if author_id in top_1000_authors:
                writer.writerow({'id': paper_id, 'author_id': author_id})

print(f"The mapping table has been created and saved to '{output_file}'.")
