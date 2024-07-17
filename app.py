from flask import Flask, render_template, request
import json
import logging
import os
from ipynb.fs.full.MSE_24_Group_Projects import retrieve


app = Flask(__name__)

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG)

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON from {file_path}: {e}")
    return {}

# Split of the attributes of the results
def load_search_results(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [
                {'query_number': line.split('\t')[0], 'rank': line.split('\t')[1], 
                 'url': line.split('\t')[2], 'score': line.split('\t')[3], 'filter': line.split('\t')[4]}
                for line in f if len(line.split('\t')) == 5
            ]
    except Exception as e:
        logging.error(f"Error loading search results from {file_path}: {e}")
    return []

ranking = retrieve('tübingen location', load_json_file('index.json'))

# Get the Image of each document
def find_image(index):
    supported_formats = ['.svg', '.png', '.jpg', '.jpeg']
    for fmt in supported_formats:
        img_path = f'static/pictures/{index}{fmt}'
        if os.path.exists(img_path):
            return img_path
    return 'static/pictures/default_picture.jpg'

# Path search results
search_results = load_search_results('src/search_results.txt')
# Path categories
categories = load_json_file('static/categories.json')

#Get title and description
def get_info(index):
    json_path = f'static/documents/{index}.json'
    data = load_json_file(json_path)
    title = data.get('title', 'No title')
    description = data.get('description', 'No description')
    image_url = find_image(index)
    return title, description, image_url

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = []
    for idx, result in enumerate(search_results):
        title, description, image_url = get_info(idx)
        results.append({'url': result['url'], 'title': title, 'snippet': description, 'image': image_url})
    return render_template('results.html', query=query, results=results, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
