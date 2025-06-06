import aioredis
from src.config import Config
# from redis.asyncio as aioredis

JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(
    # host=Config.REDIS_HOST,
    # port=Config.REDIS_PORT,
    # f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}",
    Config.REDIS_URL
    # db=0
)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti,value='',ex=JTI_EXPIRY)

async def token_in_blocklist(jti:str) -> bool:
    jti = await token_blocklist.get(jti)
    return jti is not None
