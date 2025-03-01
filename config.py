from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    BOT_TOKEN: str


def load_config(path: str | None = None) -> Config:
    env = Env()

    # read .env file, if it exists
    env.read_env(path)

    return Config(BOT_TOKEN=env('BOT_TOKEN'))
