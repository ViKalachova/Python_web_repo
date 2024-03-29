import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote
import connect


if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'), born_location=el.get(
                    "born_location"), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print('Автор вже існує')

    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author_name = el.get('author')
            author = Author.objects.get(fullname=author_name)
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()
            