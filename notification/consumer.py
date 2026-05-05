import time
import redis
from settings import settings


streams = ["order_completed", "refund_order"]

r = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password,
    decode_responses=True
)


for stream in streams:
    try:
        r.xgroup_create(
            name=stream,
            groupname=settings.notification_group,
            id="0",
            mkstream=True
        )
        print(f"Notification group created for stream: {stream}")
    except Exception:
        print(f"Notification group already exists for stream: {stream}")


while True:
    try:
        results = r.xreadgroup(
            groupname=settings.notification_group,
            consumername=settings.notification_consumer,
            streams={
                "order_completed": ">",
                "refund_order": ">"
            },
            count=1,
            block=5000
        )

        if results:
            for stream_name, messages in results:
                for message_id, data in messages:
                    order_id = data.get("pk", "nepoznat")

                    if stream_name == "order_completed":
                        print(
                            f"Obaveštenje: Porudžbina {order_id} je uspešno kreirana i plaćena."
                        )

                    elif stream_name == "refund_order":
                        print(
                            f"Obaveštenje: Za porudžbinu {order_id} je pokrenut refund."
                        )

                    r.xack(stream_name, settings.notification_group, message_id)

    except Exception as e:
        print(f"Notification consumer error: {e}")
        time.sleep(3)