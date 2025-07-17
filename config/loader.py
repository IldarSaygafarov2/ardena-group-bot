from dataclasses import dataclass
from typing import Optional

import environs

from config.bot_config import BotConfig
from config.db_config import DbConfig




@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config(env_path: Optional[str] = None) -> Config:
    env = environs.Env()
    env.read_env(env_path)

    return Config(
        bot=BotConfig.load_from_env(env),
        db=DbConfig.load_from_env(env),
    )


app_config = load_config()
