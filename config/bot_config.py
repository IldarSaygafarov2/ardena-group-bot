from dataclasses import dataclass

import environs


@dataclass
class BotConfig:
    token: str
    admin_chat_id: list

    @staticmethod
    def load_from_env(env: environs.Env) -> "BotConfig":
        return BotConfig(token=env.str("BOT_TOKEN"), admin_chat_id=env.list("ADMIN_CHAT_IDS", subcast=int))
