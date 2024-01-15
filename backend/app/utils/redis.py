import json
from aioredis import Redis
import logging
import os


async def get_redis_client():
    try:
        if os.getenv("PY_ENV") == "development":
            redis = await Redis(
                host="localhost",
                port=6379,
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True,
            )
        else:
            redis = Redis(
                host=os.getenv("REDIS_HOST"),
                port=6379,
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True,
                ssl=True,
                ssl_cert_reqs="none",
            )
        
        pong = await redis.ping()
        logging.info("Redis connection established", pong)
        return redis
    except:
        logging.error("Redis connection error")
        return None


async def read_pnl_from_redis(redis_client, key):
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        return json.loads(value)
    except Exception as e:
        logging.error(e)
        return None


async def write_pnl_to_redis(redis_client, key, value, ttl=900):
    try:
        if ttl:
            await redis_client.set(key, value, ex=ttl)
        else:
            await redis_client.set(key, value)
    except Exception as e:
        logging.error(e)
        return None