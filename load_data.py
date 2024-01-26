import os
import json
from mongoengine import connect
from models import Quote, Author
from dotenv import load_dotenv

load_dotenv()

# Отримання значень змінних середовища
mongo_uri = os.getenv("MONGO_URI")
password = os.getenv("PASSWORD")

try:
    connect(db='your_database', host=mongo_uri.replace("<password>", password))
    print("Connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

current_directory = os.path.dirname(os.path.realpath(__file__))
authors_file_path = os.path.join(current_directory, 'quotes_scraper', 'authors.json')

# Завантаження авторів та цитат з файлу authors.json
with open(authors_file_path, 'r', encoding='utf-8') as file:
    authors_data = json.load(file)
    for author_data in authors_data:
        author = Author(fullname=author_data['author'])
        author.save()

        # Створення об'єкта Quote та пов'язання його з автором
        quote = Quote(quote=author_data['text'], author=author)
        quote.tags = author_data.get('tags', [])
        quote.save()

        print(f"Author '{author.fullname}' and associated quote loaded.")

