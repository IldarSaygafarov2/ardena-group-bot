from dataclasses import dataclass

import environs
from sqlalchemy.engine.url import URL


@dataclass
class DbConfig:
    driver: str
    user: str
    password: str
    host: str
    port: int
    database: str

    @staticmethod
    def load_from_env(env: environs.Env) -> "DbConfig":
        return DbConfig(
            driver=env.str("DB_DRIVER"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            database=env.str("DB_NAME"),
        )

    def construct_url(self) -> str:
        return URL.create(
            drivername=f'postgresql+{self.driver}',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        ).render_as_string(hide_password=False)
