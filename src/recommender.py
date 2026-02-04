"""
Movie Recommender System
Finds similar movies based on attributes of a seen movie.
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MovieRecommender:
    '''Recommends movies based on similarity'''

    def __init__(self, data_path='data/processed/movies_cleaned.csv'):
        self.df = pd.read_csv(data_path)
        
    
    def prepare_features(self):
        # One-hot encode genres 
        self.df = pd.get_dummies(self.df, columns=['primary_genre'], prefix='genre')

        # Get all genre columns
        self.genre_cols = [col for col in self.df.columns if col.startswith('genre_')]

        # Normalize budget and year for fair comparison
        scaler = StandardScaler()
        self.df[['budget_scaled', 'year_scaled']] = scaler.fit_transform(self.df[['budget', 'year']])

        # Create feature table (genres, scaled budget, scaled year)
        self.feature_cols = self.genre_cols + ['budget_scaled', 'year_scaled']
        self.feature_matrix = self.df[self.feature_cols].values
    


