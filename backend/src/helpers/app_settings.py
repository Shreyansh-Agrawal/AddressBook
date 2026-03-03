import os


class AppSettings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./addresses.db")
