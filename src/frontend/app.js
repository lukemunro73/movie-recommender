const { createApp } = Vue;

createApp({
    
    data() {
        return {
            // What the user types in the search box
            movieInput: '',
            
            // Array to store movie recommendations from API
            recommendations: [],
            
            // Boolean to track if we're currently loading data
            loading: false,
            
            // String to store error messages
            error: '',
            
            // Store the movie title that was searched
            queriedMovie: '',
            
            // Boolean to track if user has searched at least once
            searched: false
        }
    },
    
    methods: {
        
        async getRecommendations() {
            
            // Check if input is empty
            if (!this.movieInput.trim()) {
                return;  // Exit function early
            }
            
            // Set loading to true
            this.loading = true;
            
            // Clear any previous error messages
            this.error = '';
            
            // Clear previous recommendations
            this.recommendations = [];
            
            // Mark that user has searched
            this.searched = true;
            
            // Save what they searched for (for the heading)
            this.queriedMovie = this.movieInput;
            
            try {

                // Build the API URL
                const apiUrl = `http://localhost:8000/recommend?movie=${encodeURIComponent(this.movieInput)}`;
                
                // Log to browser console
                console.log('Calling API:', apiUrl);
                
                // Makes the HTTP request to API and awaits response
                const response = await fetch(apiUrl);
                
                // Check if request was successful
                if (!response.ok) {
                    throw new Error('Movie not found or API error');
                }
                
                // The API sends JSON text, this converts it to JavaScript objects
                const data = await response.json();
                
                // Log the data for inspection
                console.log('Got movies from API:', data);
                
                // Check if API returned an error object
                if (data.error) {
                    // Set error message
                    this.error = data.error;
                } else {
                    // Updates all the v-for movie cards
                    this.recommendations = data;
                }
                
            } catch (err) {
                // Something went wrong
                console.error('Error:', err);
                
                // Set error message
                this.error = `Could not find "${this.movieInput}". Please check the spelling or try another movie.`;
                
            } finally {
                // Set loading back to false regardless of outcome
                this.loading = false;
            }
        },
        
        formatBudget(budget) {
            // Formats numbers based on locale (US format)
            return new Intl.NumberFormat('en-US').format(budget);
        }
    }
    
}).mount('#app');