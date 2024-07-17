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
def find_image(index):
    supported_formats = ['.svg', '.png', '.jpg', '.jpeg']
    for fmt in supported_formats:
        img_path = f'static/pictures/{index}{fmt}'
        if os.path.exists(img_path):
            return img_path
    return 'static/pictures/default_picture.jpg'

# Path categories
categories = load_json_file('static/categories.json')

# Get title and description
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

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query') if request.method == 'GET' else request.form['query']
    ranklist = [
    [0, 'https://en.wikipedia.org/wiki/Neckarfront', 4.320154330966258, 'neckarfront'],
    [1, 'https://en.wikipedia.org/wiki/St._George%27s_Collegiate_Church,_T%C3%BCbingen', 4.294722935465357, 'ulrich'],
    [2, 'https://en.wikivoyage.org/wiki/T%C3%BCbingen', 2.866682863719404, 'ulrich'],
    [3, 'https://en.wikipedia.org/wiki/Friedrich_H%C3%B6lderlin', 2.1675640402040317, 'ulrich'],
    [4, 'https://en.wikipedia.org/wiki/Stuttgart', 1.5731610178940094, 'ulrich']
]
    selected_filter = request.args.get('filter') if request.method == 'GET' else request.form.get('filter')
    filter_count = Counter([result[3] for result in ranklist])
    top_filters = [word for word, count in filter_count.most_common(5)]

    results = []
    for result in ranklist:
        if selected_filter and result[3] != selected_filter:
            continue
        idx = result[0]
        title, description, image_url = get_info(idx)
        results.append({'url': result[1], 'title': title, 'snippet': description, 'image': image_url})

    return render_template('results.html', query=query, results=results, top_filters=top_filters, categories=categories)


@app.route('/filter', methods=['POST'])
def filter():
    selected_filter = request.form['filter']
    query = request.form['query']
    return redirect(url_for('search', query=query, filter=selected_filter))

if __name__ == '__main__':
    app.run(debug=True)
