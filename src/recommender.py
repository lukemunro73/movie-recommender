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
        self.prepare_features()


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
    

    def get_recommendations(self, movie_title, num_recommendations):
        """
        Get movie recommendations based on a movie title
        
        Args:
            movie_title: Title of the movie to find similar movies for
            num_recommendations: Number of recommendations to return
            
        Returns:
            DataFrame with recommended movies and their similarity scores
        """

        # Find the movie
        movie_matches = self.df[self.df['title'].str.lower() == movie_title.lower()]

        if len(movie_matches) == 0:
            print(f"Movie '{movie_title}' not found in database")
            print("Searching for similar titles...")
            similar = self.df[self.df['title'].str.contains(movie_title)]
            if len(similar) > 0:
                print(f"\nDid you mean one of these?")
                print(similar[['title', 'year', 'budget']].head(5))
            return None
        
        # Get movie's feature vector
        movie_idx = movie_matches.index
        movie_features = self.feature_matrix[movie_idx].reshape(1, -1)

        # Calculate similarity with all movies
        similarities = cosine_similarity(movie_features, self.feature_matrix)[0]
        
        # Get indices of most similar movies (excluding the searched movie itself)
        similar_indices = similarities.argsort()[::-1][1:num_recommendations+1]
        
        # Create results dataframe
        results = self.df.iloc[similar_indices][['title', 'year', 'overview', 'budget']].copy()
        results['similarity_score'] = similarities[similar_indices]

        return results


def main():

    """Example usage"""

    # Create recommender
    recommender = MovieRecommender()

    # Example 1: Get recommendations based on a movie
    recommendations = recommender.get_recommendations('Pulp Fiction', num_recommendations=5)
    if recommendations is not None:
        print("\nTop 5 similar movies:")
        print(recommendations)

if __name__ == "__main__":
    main()