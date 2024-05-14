from dataclasses import dataclass
from arq.connections import RedisSettings

@dataclass
class Config:
    BOT_TOKEN: str
    URL_WEBHOOK: str
    pool_settings: None
    POSTGRESQL: str
    POSTGRESQL_FOR_ALEMBIC: str


def load_config() -> Config:
    return Config(BOT_TOKEN='6927452893:AAE2p58FEV3oj6XfptYJcc92Uqmf53YISMM',
                  URL_WEBHOOK='https://e708-84-244-14-170.ngrok-free.app',
                  pool_settings=RedisSettings(host='127.0.0.1', port=6379),
                  POSTGRESQL='postgresql+asyncpg://postgres:356211kKmM@91.220.109.208:5432/bot',
                  POSTGRESQL_FOR_ALEMBIC='postgresql+asyncpg://postgres:356211kKmM@91.220.109.208:5432/bot')

settings = load_config()
