import logging
import os
from dataclasses import dataclass
from environs import Env


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] #%(levelname)-6s %(filename)-15s: %(lineno)-3s - %(message)s'
)

logger = logging.getLogger(__name__)


@dataclass
class Config:
    BOT_TOKEN: str
    DB_PATH: str
    EMAIL_REGEX: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env()      # read .env file, if it exists

    return Config(
        BOT_TOKEN=env('BOT_TOKEN'),
        DB_PATH=env('DB_PATH'),
        EMAIL_REGEX=env('EMAIL_REGEX'))
