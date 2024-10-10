import os
from flask import Flask, jsonify, request
from opensearchpy import OpenSearch
from dotenv import load_dotenv
import requests
from flask_cors import CORS



# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Get Pexels API key from the environment variable
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')


# Initialize OpenSearch client
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,
    timeout=30,
    max_retries=3,
    retry_on_timeout=True
)

INDEX_NAME = 'epirecipes'


# Get recipe details by ID and image by title
@app.route('/recipe_with_image/<id>', methods=['GET'])
def get_recipe_with_image(id):
    try:
        # Retrieve the document from OpenSearch by ID
        recipe_response = client.get(index=INDEX_NAME, id=id)
        if '_source' not in recipe_response:
            return jsonify({'error': 'Recipe not found'}), 404
        
        recipe_data = recipe_response['_source']
        title = recipe_data.get('title', '').strip()  # Get title and strip extra spaces
        print("this is title" + title)

        # Fetch image from Pexels API by title
        if not PEXELS_API_KEY:
            return jsonify({'error': 'API key is missing'}), 500

        headers = {'Authorization': PEXELS_API_KEY}
        url = f"https://api.pexels.com/v1/search?query={title}&per_page=1"
        image_response = requests.get(url, headers=headers)

        # print("this is image response" + image_response)

        if image_response.status_code == 200:

            image_data = image_response.json()
            # print("this is image data" + image_data)
            if image_data['photos']:
                # Extract the medium-sized image URL from the response
                image_url = image_data['photos'][0]['src']['original']
                recipe_data['image_url'] = image_url
            else:
                recipe_data['image_url'] = None  # No image found
        else:
            recipe_data['image_url'] = None  # Image fetch failed

        # Return the combined recipe data with image URL
        return jsonify(recipe_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 404




# Search for recipes based on keywords
@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))

    body = {
        "from": (page - 1) * size,
        "size": size,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title"]
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=body)
    hits = response['hits']['hits']

    results = [{'id': hit['_id'], 'title': hit['_source']['title']} for hit in hits]
    return jsonify({
        'total': response['hits']['total']['value'],
        'results': results,
        'page': page,
        'size': size
    })

# Filter recipes by ingredients, cuisine, preparation time
@app.route('/filter', methods=['GET'])
def filter_recipes():
    ingredients = request.args.getlist('ingredients')
    cuisine = request.args.get('cuisine', None)
    prep_time = request.args.get('prep_time', None)
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))

    must_queries = []
    if ingredients:
        must_queries.append({
            "terms": {
                "ingredients": ingredients
            }
        })
    if cuisine:
        must_queries.append({
            "match": {
                "cuisine": cuisine
            }
        })
    if prep_time:
        must_queries.append({
            "range": {
                "prep_time": {"lte": prep_time}
            }
        })

    body = {
        "from": (page - 1) * size,
        "size": size,
        "query": {
            "bool": {
                "must": must_queries
            }
        }
    }

    response = client.search(index=INDEX_NAME, body=body)
    hits = response['hits']['hits']

    results = [{'id': hit['_id'], 'title': hit['_source']['title'], 'ingredients': hit['_source']['ingredients']} for hit in hits]
    return jsonify({
        'total': response['hits']['total']['value'],
        'results': results,
        'page': page,
        'size': size
    })

# Pagination endpoint for search results
@app.route('/paginate', methods=['GET'])
def paginate_recipes():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))

    body = {
        "from": (page - 1) * size,
        "size": size,
        "query": {
            "match_all": {}
        }
    }

    response = client.search(index=INDEX_NAME, body=body)
    hits = response['hits']['hits']

    results = [{'id': hit['_id'], 'title': hit['_source']['title'], 'ingredients': hit['_source']['ingredients']} for hit in hits]
    return jsonify({
        'total': response['hits']['total']['value'],
        'results': results,
        'page': page,
        'size': size
    })

if __name__ == '__main__':
    app.run(debug=True)
