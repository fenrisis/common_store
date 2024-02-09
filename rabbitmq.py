import json
import decimal
import pika

def default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)  # или float(obj) для конвертации в число с плавающей точкой
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


def send_order_to_queue(order_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='new_orders')

    # Использование кастомного энкодера для обработки Decimal
    body = json.dumps(order_data, default=default)

    channel.basic_publish(exchange='',
                          routing_key='new_orders',
                          body=body)

    print(" [x] Sent 'Order Created' message to 'new_orders' queue")
    connection.close()


def send_update_order_to_queue(order_id, status):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='order_updates')

    order_update_data = {
        'order_id': order_id,
        'status': status
    }

    body = json.dumps(order_update_data, default=default)

    channel.basic_publish(exchange='',
                          routing_key='order_updates',
                          body=body)

    print(f" [x] Sent 'Order Status Update' message to 'order_updates' queue: {order_update_data}")
    connection.close()