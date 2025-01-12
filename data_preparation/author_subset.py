import csv

# Input and output file paths
input_file = 'output.csv'
subset_output_file = 'author_subset.csv'

# Open input and output files
with open(input_file, 'r') as infile, open(subset_output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['author_id', 'author_name', 'n_citation', 'publication_count']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header for the subset file

    for row in reader:
        # Split author_id and author_name into lists
        author_ids = row['author_id'].split(';') if row['author_id'] else []
        author_names = row['author_name'].split(';') if row['author_name'] else []
        n_citation = int(row['n_citation']) if row['n_citation'] else 0
        publication_count = 1  # Each row corresponds to one publication

        # Ensure the lengths of author_ids and author_names match
        if len(author_ids) == len(author_names):
            for author_id, author_name in zip(author_ids, author_names):
                writer.writerow({
                    'author_id': author_id,
                    'author_name': author_name,
                    'n_citation': n_citation,
                    'publication_count': publication_count
                })

print(f"The subset dataset with publication counts has been created and saved to '{subset_output_file}'.")
