from redis import asyncio as aioredis
from app.config import setting

class RedisManager:
    def __init__(self, host: str, port: int):
        self.url = f"redis://{host}:{port}"
        self.client: aioredis.Redis | None = None

    def get_client(self) -> aioredis.Redis:
        if self.client is None:
            self.client = aioredis.from_url(
                self.url, 
                decode_responses=True,
                encoding="utf-8"
            )
        return self.client

    async def set_verification_token(self, token: str, email: str, expire: int = 86400):
        client = self.get_client()
        await client.set(f"verification:{token}", email, ex=expire)

    async def get_email(self, token: str) -> str | None:
        client = self.get_client()
        email = await client.get(f"verification:{token}")
        return email
    
    async def delete(self, oper_key: str, value_key: str):
        client = self.get_client()
        response = await client.delete(f"{oper_key}:{value_key}")
        return response

    async def close(self):
        if self.client:
            await self.client.close()

redis_manager = RedisManager(host=setting.REDIS_HOST, port=setting.REDIS_PORT)