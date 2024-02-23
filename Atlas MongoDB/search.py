from typing import Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_tags(tags: str) -> list[list[Any]]:
    all_tags = tags.split(',')
    result = []
    for el in all_tags:
        quotes = Quote.objects(tags__iregex=el)
        result.append([q.quote for q in quotes])
    return result

@cache
def find_by_author(author: str) -> list[list[Any]]:
    authors = Author.objects(fullname__iregex=author)
    result = []
    for a in authors:
        quotes = Quote.objects(author=a)
        result.append([q.quote for q in quotes])
    return result



while True:
    user_input = input("Введіть команду (name/tag/tags/exit): ").strip().split(':')
    command = user_input[0]
    value = user_input[1]
    if command == 'exit':
        break
    elif command == 'name':
        result = find_by_author(value)
        print(f'{value}: {result}')
    elif command == 'tag':
        result = find_by_tag(value)
        print(f'{value}: {result}')
    elif command == 'tags':
        result = find_by_tags(value)
        print(f'{value}: {result}')
