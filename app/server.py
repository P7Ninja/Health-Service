from fastapi import FastAPI
from dotenv import dotenv_values

from healthservice import SQLHealthDB, HealthService

cfg = dotenv_values(".env")

app = FastAPI()
db = SQLHealthDB(cfg)
service = HealthService(app, db, cfg)

service.configure_database()
service.configure_routes()