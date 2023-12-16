from aioredis import Redis
import logging
import os
async def get_redis_client():
    try:
        redis = await Redis(
            host="localhost", port=6379, password=os.getenv("REDIS_PASSWORD"), decode_responses=True
        ) if os.getenv("DEV_MODE") else await Redis(
            host=os.getenv("REDIS_HOST"), port=6379, password=os.getenv("REDIS_PASSWORD"), decode_responses=True, ssl=True, ssl_cert_reqs="none"
        )
        return redis
    except:
        logging.error("Redis connection error")
        return None