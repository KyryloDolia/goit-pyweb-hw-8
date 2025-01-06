import pika
from bson import ObjectId
from contact_model import Contact

RABBITMQ_QUEUE = 'email_queue'


def send_email(contact):
    print(f"[Consumer] Sending email to {contact.email}...")
    return True


def process_message(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    print(f"[Consumer] Received contact ID: {contact_id}")

    contact = Contact.objects(id=ObjectId(contact_id)).first()
    if not contact:
        print(f"[Consumer] Contact with ID {contact_id} not found.")
        return

    if send_email(contact):
        contact.email_sent = True
        contact.save()
        print(f"[Consumer] Email sent to {contact.email}. Updated in DB.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)

    print("[Consumer] Waiting for messages...")
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
