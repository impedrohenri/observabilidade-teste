import secrets
import redis.asyncio as redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=0,
    decode_responses=True
)


CONVITE_TTL_SECONDS = 30 * 24 * 60 * 60  # 30 dias

class ConviteService:

    async def gerar_codigo_convite(self) -> str:
        while True:
            codigo_convite = secrets.token_urlsafe(8)
            chave = f"convite:{codigo_convite}"

            criado = await redis_client.set(
                chave,
                "valido",
                ex=CONVITE_TTL_SECONDS,
                nx=True
            )

            if criado:
                return codigo_convite

    async def validar_codigo(self, codigo: str) -> bool:
        chave = f"convite:{codigo}"

        
        valor = await redis_client.getdel(chave)

        return valor is not None
