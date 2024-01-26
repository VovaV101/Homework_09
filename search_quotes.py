import os
from mongoengine import connect
from models import Quote, Author
from dotenv import load_dotenv

load_dotenv()

# Отримання значень змінних середовища
mongo_uri = os.getenv("MONGO_URI")
password = os.getenv("PASSWORD")

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    connect(db='your_database', host=mongo_uri.replace("<password>", password))
    print("Connected to MongoDB.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

def print_quotes(quotes):
    if not quotes:
        print("Немає відповідних цитат.")
    else:
        for quote in quotes:
            print(quote.quote)

while True:
    user_input = input("Введіть команду: ").split(':')

    if len(user_input) >= 1:
        command = user_input[0].strip().lower()

        if command == 'name':
            if len(user_input) >= 2:
                value = user_input[1].strip()
                author = Author.objects(fullname=value).first()
                print_quotes(Quote.objects(author=author))
            else:
                print("Неправильний формат команди. Спробуйте ще раз.")
        elif command == 'tag':
            if len(user_input) >= 2:
                value = user_input[1].strip()
                print_quotes(Quote.objects(tags=value))
            else:
                print("Неправильний формат команди. Спробуйте ще раз.")
        elif command == 'tags':
            if len(user_input) >= 2:
                value = user_input[1].strip()
                tag_list = value.split(',')
                print_quotes(Quote.objects(tags__in=tag_list))
            else:
                print("Неправильний формат команди. Спробуйте ще раз.")
        elif command == 'exit':
            print("Завершення роботи.")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")
    else:
        print("Неправильний формат команди. Спробуйте ще раз.")
