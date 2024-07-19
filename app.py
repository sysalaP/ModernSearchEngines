from flask import Flask, render_template, request, redirect, url_for
import json
import logging
import os
from collections import Counter

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

# Get the Image of each document
def find_image(doc_number):
    supported_formats = ['.svg', '.png', '.jpg', '.jpeg']
    for fmt in supported_formats:
        img_path = f'static/images/{doc_number}{fmt}'
        if os.path.exists(img_path):
            return img_path
    return 'static/images/default_picture.jpg'

# Path categories
categories = load_json_file('static/categories.json')
document_index = load_json_file('index.json')

# Get title and description
def get_info(doc_number):
    json_path = f'static/documents/{doc_number}.json'
    data = load_json_file(json_path)
    title = data.get('title', 'No title')
    description = data.get('description', 'No description')
    image_url = find_image(doc_number)
    return title, description, image_url

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query') if request.method == 'GET' else request.form['query']
    logging.debug(f"Received search query: {query}")
    ranklist = retrieve(query, document_index)
    selected_filter = request.args.get('filter') if request.method == 'GET' else request.form.get('filter')
    filter_count = Counter([result[3] for result in ranklist])
    top_filters = [word for word, count in filter_count.most_common(5)]

    results = []
    for result in ranklist:
        if selected_filter and result[3] != selected_filter:
            continue
        idx = result[4]
        title, description, image_url = get_info(idx)
        results.append({'url': result[1], 'title': title, 'snippet': description, 'image': image_url})
        logging.debug(f"Appended result: {results[-1]}")

    return render_template('results.html', query=query, results=results, top_filters=top_filters, categories=categories)

@app.route('/filter', methods=['POST'])
def filter():
    selected_filter = request.form['filter']
    query = request.form['query']
    return redirect(url_for('search', query=query, filter=selected_filter))

if __name__ == '__main__':
    app.run(debug=True)
