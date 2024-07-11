from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
import logging

app = Flask(__name__)

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG)

def fetch_url_data(url):
    try:
        response = requests.get(url, verify=False)  # SSL-Verifikation deaktivieren
        if response.status_code == 200:
            return response.text
        else:
            logging.error(f"Error fetching {url}: Status code {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').text if soup.find('title') else 'No title'
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc['content'] if meta_desc else 'No description'
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    image_url = og_image['content'] if og_image else 'static/pictures/default_picture.jpg'
    return title, description, image_url

def load_search_results(file_path):
    search_results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 4:
                    query_number, rank, url, score = parts
                    search_results.append({
                        'query_number': query_number,
                        'rank': rank,
                        'url': url,
                        'score': score
                    })
        logging.info(f"Loaded {len(search_results)} search results")
    except Exception as e:
        logging.error(f"Error loading search results from {file_path}: {e}")
    return search_results

def load_categories(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            categories = json.load(f)
        logging.info(f"Loaded categories from {file_path}")
        return categories
    except Exception as e:
        logging.error(f"Error loading categories from {file_path}: {e}")
        return {}

# Pfad zur Textdatei mit den Suchergebnissen
search_results_file = 'src/search_results.txt'
search_results = load_search_results(search_results_file)

# Pfad zur JSON-Datei mit den Kategorien
categories_file = 'src/categories.json'
categories = load_categories(categories_file)

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Filter the search results based on the query
    results = []
    for result in search_results:
        url = result['url']
        html = fetch_url_data(url)
        if html:
            title, description, image_url = extract_info(html)
            results.append({
                'url': url,
                'title': title,
                'snippet': description,
                'image': image_url
            })
    return render_template('results.html', query=query, results=results, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
