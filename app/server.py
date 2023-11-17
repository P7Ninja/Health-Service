from fastapi import FastAPI
from dotenv import dotenv_values

from healthservice import SQLHealthDB, HealthService
import os

cfg = os.environ

app = FastAPI()
db = SQLHealthDB(cfg)
service = HealthService(app, db, cfg)

service.configure_database()
service.configure_routes()