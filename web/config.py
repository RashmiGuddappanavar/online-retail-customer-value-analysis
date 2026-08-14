import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "online-retail-secret-key-2026")
    PROCESSED_DIR = PROCESSED_DATA_DIR
    DB_HOST = os.getenv("DB_HOST", None)
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "online_retail_analytics")
    DB_USER = os.getenv("DB_USER", None)
    DB_PASSWORD = os.getenv("DB_PASSWORD", None)
