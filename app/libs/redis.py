from os import getenv as env

import redis

pool = redis.ConnectionPool(
    host=env("REDIS_HOST"),
    port=env("REDIS_PORT"),
    password=env("REDIS_PASSWORD"),
    decode_responses=True,
)

redis = redis.Redis(
    connection_pool=pool,
    charset="utf-8",
)
