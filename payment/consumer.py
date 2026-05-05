from database import redis
from main import Order
import time

key = 'refund_order'
group = 'payment-group'
consumer = 'payment-consumer-1'

try:
    redis.xgroup_create(key, group, id='0', mkstream=True)
except Exception:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(
            groupname=group,
            consumername=consumer,
            streams={key: '>'},
            count=1,
            block=5000
        )

        if results:
            for result in results:
                messages = result[1]

                for message_id, message_data in messages:
                    try:
                        order = Order.get(message_data['pk'])
                        order.status = 'refunded'
                        order.save()

                        print(f"Order {order.pk} successfully refunded.")

                    except Exception as e:
                        print(f"Could not find order to refund: {e}")

                    redis.xack(key, group, message_id)

    except Exception as e:
        print(f"Consumer error: {e}")
        time.sleep(3)