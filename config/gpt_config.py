from dataclasses import dataclass

from environs import Env


@dataclass
class GptConfig:
    api_key: str
    model: str

    @staticmethod
    def from_env(env: Env) -> "GptConfig":
        return GptConfig(
            api_key=env.str("GPT_API_KEY"),
            model=env.str("OPENAI_MODEL", "gpt-3.5-turbo"),
        )