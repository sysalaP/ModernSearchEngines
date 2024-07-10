from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_url_data(url):
    try:
        response = requests.get(url, verify=False)  # SSL-Verifikation deaktivieren
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').text if soup.find('title') else 'No title'
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc['content'] if meta_desc else 'No description'
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    image_url = og_image['content'] if og_image else 'static/tuebingen.jpg'
    return title, description, image_url

urls = [
    "https://www.tuebingen.de/en/3521.html",
    "https://www.komoot.com/guide/355570/castles-in-tuebingen-district",
    "https://www.unimuseum.uni-tuebingen.de/en/museum-at-hohentuebingen-castle",
    "https://www.kreis-tuebingen.de/Startseite",
    "https://www.swr.de/swraktuell/baden-wuerttemberg/tuebingen/abistreich-in-tuebingen-eskaliert-102.html",
    "https://www.swtue.de/baeder/freibad.html"

]

categories = {
    "Education & Research": ["University of Tübingen", "Study Programs", "Research", "Libraries", "Student Life", "Educational Tours"],
    "Culture & Arts": ["Tübingen Attractions", "Festivals", "Art Galleries", "Music and Theater", "Historical Landmarks", "Museums"],
    "Nature & Environment": ["Parks and Gardens", "Hiking Trails", "Nature Reserves", "River Cruises", "Environmental Initiatives", "Botanic Gardens"],
    "Society & Lifestyle": ["Food and Drinks", "Local Cuisine", "Shopping", "Nightlife", "Accommodation", "Transportation"]
}

@app.route('/')
def index():
    return render_template('index.html', categories=categories)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = []

    for url in urls:
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