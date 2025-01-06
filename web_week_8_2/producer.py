import pika
from faker import Faker
from contact_model import Contact

RABBITMQ_QUEUE = 'email_queue'


def generate_fake_contacts(count=10):
    fake = Faker()
    contacts = []
    for _ in range(count):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        contact.save()
        contacts.append(contact)
    return contacts


def send_contacts_to_queue(contacts):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    for contact in contacts:
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=str(contact.id)
        )
        print(f"[Producer] Contact {contact.id} placed in queue.")

    connection.close()


if __name__ == '__main__':
    num_contacts = 2
    contacts = generate_fake_contacts(num_contacts)
    print(f"[Producer] {num_contacts} contacts generated.")

    send_contacts_to_queue(contacts)
    print("[Producer] All contacts sent to queue.")
