from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

DATABASE_URL = settings.database_url

# 如果使用 pgbouncer，需要禁用 prepared statement 缓存
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "statement_cache_size": 0,  # 禁用 prepared statement 缓存，兼容 pgbouncer
    }
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# 用于依赖注入
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
