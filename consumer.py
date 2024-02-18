import pika
import json
from sqlalchemy import create_engine, update, select
from sqlalchemy.orm import sessionmaker
from models.models import orders
from database import SessionLocal



def on_order_received(ch, method, properties, body):
    order_data = json.loads(body)
    print("Received order update:", order_data)

    order_id = order_data.get('order_id')
    new_status = order_data.get('status')

    if not all([order_id, new_status]):
        print("Order data is incomplete.")
        return

    # Использование SessionLocal для создания сессии
    with SessionLocal() as session:
        stmt = update(orders).where(orders.c.order_id == order_id).values(status=new_status)
        result = session.execute(stmt)
        if result.rowcount:
            session.commit()
            print(f"Order {order_id} status updated to {new_status}.")
        else:
            print(f"Order {order_id} not found.")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='order_updates')

    channel.basic_consume(queue='order_updates', on_message_callback=on_order_received, auto_ack=True)

    print(' [*] Waiting for order updates. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()