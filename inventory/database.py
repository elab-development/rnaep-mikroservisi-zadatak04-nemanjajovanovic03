from redis_om import get_redis_connection
from settings import settings


redis = get_redis_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password,
    decode_responses=True
)