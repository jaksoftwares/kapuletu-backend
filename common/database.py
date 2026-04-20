import os
import psycopg2
from common.config import get_config

def get_db_connection():
    config = get_config()
    conn = psycopg2.connect(config.DATABASE_URL)
    return conn
