from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import config

url = f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_dbname}"


engine = create_async_engine(url, echo=config.db_echo)
sessionmaker = async_sessionmaker(engine, autocommit=False, autoflush=False)


async def make_session():
    async with sessionmaker() as session:
        yield session
