import ijson
import time
import csv
import numpy as np
from decimal import Decimal

start = time.process_time()

count = 0

# Open the input JSON file and output CSV file
with open('dblp.v12.json', "rb") as f, open("output.csv", "w", newline="") as csvfile:
    fieldnames = [
        'id', 'title', 'year', 'author_name', 'author_org', 'author_id',
        'n_citation', 'doc_type', 'reference_count', 'references',
        'venue_id', 'venue_name', 'venue_type', 'doi', 'keyword', 'weight',
        'indexed_keyword', 'inverted_index', 'publisher', 'volume', 'issue'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, element in enumerate(ijson.items(f, "item")):
        try:
            paper = {
                'id': element.get('id', np.nan),
                'title': element.get('title', np.nan),
                'year': element.get('year', np.nan),
                'n_citation': element.get('n_citation', np.nan),
                'doc_type': element.get('doc_type', np.nan),
                'publisher': element.get('publisher', np.nan),
                'volume': element.get('volume', np.nan),
                'issue': element.get('issue', np.nan)
            }

            # Extract author information
            authors = element.get('authors', [])
            paper['author_name'] = ';'.join(a.get('name', '') for a in authors)
            paper['author_org'] = ';'.join(a.get('org', '') for a in authors)
            paper['author_id'] = ';'.join(str(a.get('id', np.nan)) for a in authors)

            # Extract references
            references = element.get('references', [])
            paper['reference_count'] = len(references) if references else np.nan
            paper['references'] = ';'.join(map(str, references)) if references else np.nan

            # Extract venue information
            venue = element.get('venue', {})
            paper['venue_id'] = venue.get('id', np.nan)
            paper['venue_name'] = venue.get('raw', np.nan)
            paper['venue_type'] = venue.get('type', np.nan)

            # Extract DOI
            doi = element.get('doi')
            paper['doi'] = f"https://doi.org/{doi}" if doi else np.nan

            # Extract fields of study
            fos = element.get('fos', [])
            paper['keyword'] = ';'.join(f.get('name', '') for f in fos)
            paper['weight'] = ';'.join(str(f.get('w', np.nan)) for f in fos)

            # Extract indexed abstract
            indexed_abstract = element.get('indexed_abstract', {}).get('InvertedIndex', {})
            paper['indexed_keyword'] = ';'.join(indexed_abstract.keys())
            paper['inverted_index'] = ';'.join(map(str, indexed_abstract.values()))

            # Write row to CSV
            writer.writerow(paper)

            count += 1
            if count % 4800 == 0:
                print(f"{count} rows processed in {round(time.process_time() - start, 2)} seconds")

        except Exception as e:
            print(f"Error processing element {i}: {e}")

print(f"Completed processing {count} rows in {round(time.process_time() - start, 2)} seconds.")
