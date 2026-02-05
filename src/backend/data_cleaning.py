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

df['primary_genre'] = df['genres'].apply(extract_primary_genre)

df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year
df = df.dropna(subset=['year'])
df['year'] = df['year'].astype(int)

df = df[df['vote_count'] >= 500]

df_clean = df[['id', 'title', 'primary_genre', 'overview', 'budget', 'year']]

df_clean = df_clean.set_index('id')


print(f"\nFirst rows:\n{df_clean.head()}")
print(df_clean.shape)

df_clean.to_csv('data/processed/movies_cleaned.csv', index=False)