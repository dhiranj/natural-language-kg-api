import pandas as pd 

# Load the data directly from the provided file path
data = pd.read_csv('output.csv')

# Ensure necessary columns for the analysis are present
required_columns = ['author_name', 'n_citation']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The dataset must contain the following columns: {required_columns}")

# Split authors and expand the data to analyze individual contributions
authors_data = data[['author_name', 'n_citation']].dropna()
authors_data['n_citation'] = authors_data['n_citation'].fillna(0).astype(int)

# Explode authors into individual rows
authors_data = authors_data.assign(author_name=authors_data['author_name'].str.split(';')).explode('author_name')

# Group by author and aggregate metrics
author_stats = authors_data.groupby('author_name').agg(
    total_citations=('n_citation', 'sum'),
    publication_count=('n_citation', 'count')
).reset_index()

# Rank authors based on total citations and number of publications
author_stats['rank'] = author_stats['total_citations'].rank(ascending=False, method='dense')

# Sort by rank and select the top 1,000 authors
top_authors = author_stats.sort_values(by=['total_citations', 'publication_count'], ascending=[False, False]).head(1000)
# Display the top authors
print("Top 5 Computer Scientists (Sample Output):")
print(top_authors.head(5))

# Save the results to a CSV file for further exploration
top_authors.to_csv('top_1000_computer_scientists.csv', index=False)
print("The top 1,000 computer scientists have been saved to 'top_1000_computer_scientists.csv'.")
