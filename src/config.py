import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

YANDEX_ID = os.environ.get('YANDEX_ID')
YANDEX_KEY = os.environ.get('YANDEX_KEY')
YANDEX_REGION = os.environ.get('YANDEX_REGION')
