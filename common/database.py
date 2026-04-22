import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from common.config import get_config

config = get_config()

# Using pooled connections for better performance in Lambda
# (Though in pure serverless, connection pooling should be handled carefully)
engine = create_engine(
    config.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    connect_args={"sslmode": "require"} if "localhost" not in config.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
