from mongoengine import Document, StringField, BooleanField, connect

connect('email_contacts_db', host='localhost', port=27017)

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    email_sent = BooleanField(default=False)
    phone = StringField()

    def __str__(self):
        return f"{self.full_name} ({self.email})"
