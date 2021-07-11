from os import environ

from redis import StrictRedis

redis_url = environ.get('REDIS_URL', None)

if redis_url:
    redis = StrictRedis.from_url(redis_url, decode_responses=True)
else:
    redis = StrictRedis(
        host=environ.get('REDIS_HOST'),
        port=int(environ.get('REDIS_PORT')),
        db=int(environ.get('REDIS_DB')),
        password=environ.get('REDIS_PASSWORD', None),
        decode_responses=True,
    )
