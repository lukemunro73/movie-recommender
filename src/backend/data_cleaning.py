import pandas as pd
import ast

def extract_primary_genre(genres_str):
    """Extract the first/primary genre name"""
    
    try:
        genres_list = ast.literal_eval(str(genres_str))
        if genres_list and len(genres_list) > 0:
            return genres_list[0]['name']
        return 'Unknown'
    except:
        return 'Unknown'

df = pd.read_csv('data/raw/movies_metadata.csv')

# Change original genres to primary genre column
df['primary_genre'] = df['genres'].apply(extract_primary_genre)

# Change release date column to just year
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce') 
df['year'] = df['release_date'].dt.year 
df = df.dropna(subset=['year']) 
df['year'] = df['year'].astype(int)

# Remove movies with very low vote counts
df = df[df['vote_count'] >= 500] 

# Select necessary columns for clean dataset
df_clean = df[['id', 'title', 'primary_genre', 'overview', 'budget', 'year']]

# Set id to index
df_clean = df_clean.set_index('id') 

# Test processing
print(f"\nFirst rows:\n{df_clean.head()}")
print(df_clean.shape)

counts = df_clean["title"].value_counts()
print(counts[counts > 1])

# Add clean data to processed data path
df_clean.to_csv('data/processed/movies_cleaned.csv', index=False) # create new dataset