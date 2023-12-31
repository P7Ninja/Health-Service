from fastapi import FastAPI
from dotenv import dotenv_values

from healthservice import SQLHealthDB, HealthService
import os

cfg = dict()
if os.path.exists(".env"):
    cfg = dotenv_values(".env")

cfg["DB_CONN"] = os.environ.get("DB_CONN", cfg.get("DB_CONN", None))

app = FastAPI()
db = SQLHealthDB(cfg)
service = HealthService(app, db, cfg)

service.configure_database()
service.configure_routes()