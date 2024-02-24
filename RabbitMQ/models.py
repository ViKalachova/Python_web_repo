from mongoengine import Document, StringField, BooleanField
import connect

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)
