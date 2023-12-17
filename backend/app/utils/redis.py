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
        print("Redis connection established", pong)
        return redis
    except:
        logging.error("Redis connection error")
        return None
