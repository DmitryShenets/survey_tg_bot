import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    REDIS_HOST: str = os.environ.get('REDIS_HOST')
    REDIS_PORT: int = os.environ.get('REDIS_PORT')
    REDIS_DB: int = os.environ.get('REDIS_DB')
    TOKEN: str = os.environ.get('TG_BOT_TOKEN')


CONFIG = Config()
