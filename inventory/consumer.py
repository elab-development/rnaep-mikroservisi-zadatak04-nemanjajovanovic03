from database import redis
from main import Product
import time

key = 'order_completed'
group = 'inventory-group'
consumer = 'inventory-consumer-1'

try:
    redis.xgroup_create(key, group, id='0', mkstream=True)
except:
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
                stream_name = result[0]
                messages = result[1]

                for message_id, obj in messages:
                    try:
                        product = Product.get(obj['product_id'])
                        product.quantity -= int(obj['quantity'])
                        product.save()

                        print(f"Stock updated for {product.name}")

                    except Exception as e:
                        redis.xadd('refund_order', obj, '*')
                        print(f"Error: {e}")

                    redis.xack(key, group, message_id)

    except Exception as e:
        print(str(e))
        time.sleep(3)