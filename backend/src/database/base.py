from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from helpers.app_settings import AppSettings

connect_args = {"check_same_thread": False} if ":memory:" not in AppSettings.DATABASE_URL and "sqlite" in AppSettings.DATABASE_URL else {}
engine = create_engine(
    AppSettings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)
Base = declarative_base()
