import pandas as pd
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}],
    http_compress=True,
    timeout=30,
    max_retries=3,
    retry_on_timeout=True
)

INDEX_NAME = 'epirecipes'

# Define the OpenSearch index mapping
mapping = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "rating": {"type": "float"},
            "calories": {"type": "integer"},
            "protein": {"type": "integer"},
            "fat": {"type": "integer"},
            "sodium": {"type": "integer"},
            "#cakeweek": {"type": "integer"},
            "#wasteless": {"type": "integer"},
            "22-minute meals": {"type": "integer"},
            "3-ingredient recipes": {"type": "integer"},
            "30 days of groceries": {"type": "integer"},
            "advance prep required": {"type": "integer"},
            "alabama": {"type": "integer"},
            "alaska": {"type": "integer"},
            "alcoholic": {"type": "integer"},
            "almond": {"type": "integer"},
            "amaretto": {"type": "integer"},
            "anchovy": {"type": "integer"},
            "anise": {"type": "integer"},
            "anniversary": {"type": "integer"},
            "anthony bourdain": {"type": "integer"},
            "aperitif": {"type": "integer"},
            "appetizer": {"type": "integer"},
        }
    }
}

# Create the index
if not client.indices.exists(index=INDEX_NAME):
    client.indices.create(index=INDEX_NAME, body=mapping)

# Load the dataset and index documents
df = pd.read_csv('epi_recipes.csv')

df.fillna(0, inplace=True)

for idx, row in df.iterrows():
    doc = {
        'title': row['title'],
        'rating': row['rating'],
        'calories': row['calories'],
        'protein': row['protein'],
        'fat': row['fat'],
        'sodium': row['sodium'],
        '#cakeweek': row['#cakeweek'],
        '#wasteless': row['#wasteless'],
        '22-minute meals': row['22-minute meals'],
        '3-ingredient recipes': row['3-ingredient recipes'],
        '30 days of groceries': row['30 days of groceries'],
        'advance prep required': row['advance prep required'],
        'alabama': row['alabama'],
        'alaska': row['alaska'],
        'alcoholic': row['alcoholic'],
        'almond': row['almond'],
        'amaretto': row['amaretto'],
        'anchovy': row['anchovy'],
        'anise': row['anise'],
        'anniversary': row['anniversary'],
        'anthony bourdain': row['anthony bourdain'],
        'aperitif': row['aperitif'],
        'appetizer': row['appetizer'],
        

    }
    client.index(index=INDEX_NAME, id=idx, body=doc)

print('Data indexing complete.')
