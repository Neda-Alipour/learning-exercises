from redis.asyncio import Redis


from app.config import db_setting

_token_blacllist = Redis(
    host=db_setting.REDIS_HOST,
    port=db_setting.REDIS_PORT,
    db=0,
)


async def add_jti_to_blacklist(jti: str):
    await _token_blacllist.set(jti, "blacklisted")


async def is_jti_blacklisted(jti: str) -> bool:
    return await _token_blacllist.exists(jti)