import pika
import json
from faker import Faker
from models import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()


channel.queue_declare(queue='contacts')

fake = Faker()
for _ in range(10):
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()

    channel.basic_publish(exchange='', routing_key='contacts', body=json.dumps({'contact_id': str(contact.id)}))
    print(f"Додано контакт: {full_name}, Email: {email}")

connection.close()