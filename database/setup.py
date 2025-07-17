from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config.db_config import DbConfig


def create_engine(db: DbConfig, echo: bool = False):
    return create_async_engine(
        db.construct_url(),
        echo=echo,
        future=True,
        pool_pre_ping=True,
        max_overflow=10,
        pool_size=5,
        pool_timeout=30,
    )


def create_session_pool(engine):
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=True,
        autocommit=False,
    )
