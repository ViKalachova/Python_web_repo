import pika
import json
from models import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
channel = connection.channel()

channel.queue_declare(queue='contacts')

def callback(ch, method, properties, body):
    contact_id = json.loads(body)['contact_id']
    contact = Contact.objects.get(id=contact_id)
    print(f"Надсилаємо email до: {contact.email}")
    contact.message_sent = True
    contact.save()
    print("Статус повідомлення оновлено")


channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
