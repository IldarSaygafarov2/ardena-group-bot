from dataclasses import dataclass

import environs


@dataclass
class BotConfig:
    token: str
    admin_chat_id: int

    @staticmethod
    def load_from_env(env: environs.Env) -> "BotConfig":
        return BotConfig(token=env.str("BOT_TOKEN"), admin_chat_id=env.int("ADMIN_CHAT_ID"))
