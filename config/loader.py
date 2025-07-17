from dataclasses import dataclass
from typing import Optional

import environs

from config.bot_config import BotConfig
from config.db_config import DbConfig

CARGO_TRACKING_FIELDS = [
    'uni_in_shipment',
    'shipper',
    'destination',
    'vehicle_type',
    'date_of_dispatch',
    'current_station',
    'remaining_distance',
    'number_of_container_or_wagon',
    'arrival_date',
    'brand',
    'gross_weight',
    'net_weight',
    'places_number',
]


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
