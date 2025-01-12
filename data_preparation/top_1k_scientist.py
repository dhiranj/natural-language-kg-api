import pandas as pd

# Load the subset data
subset_file = 'author_subset.csv'
subset_data = pd.read_csv(subset_file)

# Group by author and aggregate metrics
author_stats = subset_data.groupby(['author_name', 'author_id']).agg(
    total_citations=('n_citation', 'sum'),         # Sum of citations
    publication_count=('publication_count', 'sum') # Sum of publications
).reset_index()

# Rank authors based on total citations (primary) and publication count (secondary)
author_stats['rank'] = author_stats[['total_citations', 'publication_count']].apply(
    lambda x: (-x[0], -x[1]), axis=1
).rank(method='dense').astype(int)

# Sort by rank and select the top 1,000 authors
top_authors = author_stats.sort_values(by='rank').head(1000)

# Reorder columns for better readability
top_authors = top_authors[['rank', 'author_id', 'author_name', 'total_citations', 'publication_count']]

# Save the results to a CSV file for further exploration
top_authors_file = 'top_1000_computer_scientists.csv'
top_authors.to_csv(top_authors_file, index=False)

print(f"The top 1,000 computer scientists have been saved to '{top_authors_file}'.")
