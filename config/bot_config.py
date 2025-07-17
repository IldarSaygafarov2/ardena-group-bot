from dataclasses import dataclass

import environs


@dataclass
class BotConfig:
    token: str

    @staticmethod
    def load_from_env(env: environs.Env) -> "BotConfig":
        return BotConfig(token=env.str("BOT_TOKEN"))
