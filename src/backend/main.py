"""
Movie Recommender API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommender import MovieRecommender

app = FastAPI()

# Allow website to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load recommender class
recommender = MovieRecommender() 

# Set GET endpoint 
@app.get("/recommend")
def recommend(movie, n: int = 5):
    """Get movie recommendations"""

    results = recommender.get_recommendations(movie, num_recommendations=n)
    if results is None:
        return {"error": "Movie not found"}
    
    return results.to_dict('records')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) # standard numbers for FastAPI