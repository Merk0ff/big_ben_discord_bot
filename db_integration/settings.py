from os import environ

from redis import StrictRedis


redis = StrictRedis(
    host=environ.get('REDIS_HOST'),
    port=int(environ.get('REDIS_PORT')),
    db=int(environ.get('REDIS_DB')),
    decode_responses=True,
)
