from flask import Flask, request, render_template
import threading

app = Flask(__name__)

# Dummy data for search results
search_results = [
    {"title": "Result 1", "url": "http://example.com/1", "snippet": "This is a brief description of the first result.", "image": "http://example.com/image1.jpg"},
    {"title": "Result 2", "url": "http://example.com/2", "snippet": "This is a brief description of the second result.", "image": "http://example.com/image2.jpg"}
]

# Categories and predefined queries
categories = {
    "Education & Research": ["University of Tübingen", "Study Programs", "Research", "Libraries", "Student Life", "Educational Tours"],
    "Culture & Arts": ["Tübingen Attractions", "Festivals", "Art Galleries", "Music and Theater", "Historical Landmarks", "Museums"],
    "Nature & Environment": ["Parks and Gardens", "Hiking Trails", "Nature Reserves", "River Cruises", "Environmental Initiatives", "Botanic Gardens"],
    "Society & Lifestyle": ["Food and Drinks", "Local Cuisine", "Shopping", "Nightlife", "Accommodation", "Transportation"]
}

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html', categories=categories)

# Route for search results
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = search_results  # Temporary dummy results
    return render_template('results.html', results=results, query=query, categories=categories)

# Function to start the Flask app in a separate thread
def run_flask_app():
    app.run(port=5002, debug=False, use_reloader=False)  # Debug mode and reloader disabled

# Start the Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()
