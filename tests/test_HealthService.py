import pytest
import shutil
import json
from datetime import datetime
from pytest import FixtureRequest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient

from healthservice.database import SQLHealthDB
from healthservice.database.health_schema import *
from healthservice import HealthService

@pytest.fixture
def client(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)

    db = SQLHealthDB({"DB_CONN": f"sqlite:///{db_file}"})
    app = FastAPI()
    service = HealthService(app, db, dict())
    db.startup()
    service.configure_routes()
    request.addfinalizer(lambda: db.shutdown())
    
    return TestClient(app)
    
    
def test_InsertHealthEntry(client: TestClient):
    input = {
        "userID":2,
        "dateStamp": str(datetime(2023, 11, 3, 12, 28, 18, 52000)),
        "height":170,
        "weight":70,
        "fatPercentage":20,
        "musclePercentage":80,
        "waterPercentage":60
    }
    input2 = {
        "userID":2,
        "dateStamp": str(datetime(2023, 11, 3, 12, 28, 18, 52000)),
        "height":170
    }
    input3 = {
        "userID":2,
        "dateStamp": str(datetime(2023, 11, 3, 12, 28, 18, 52000))
    }
    
    res1 = client.post("/insertHealth", content=json.dumps(input))
    assert res1.status_code == 200
    assert res1.json() == {"success": True}
    
    res2 = client.post("/insertHealth", content=json.dumps(input2))
    assert res2.status_code == 200
    assert res2.json() == {"success": True}
    
    res3 = client.post("/insertHealth", content=json.dumps(input3))
    assert res3.status_code == 400
    
    
    
def test_DeleteHealthEntry(client: TestClient):
    res1 = client.delete("/deleteHealth?id=3&userID=0")
    assert res1.status_code == 200
    assert res1.json() == {"success": True}

def test_GetUsersLatestHealthEntry(client: TestClient):
    
    health_entry = client.get("/getHealth?userID=0").json()
    res = client.get("/getHealth?userID=0")

    assert res.status_code == 200
    
    assert health_entry["userID"] == 0
    assert health_entry["dateStamp"] == "2023-11-03T12:28:18.052000" #todo cannot get this to work with a datetime


def test_GetUsersHealthEntries(client: TestClient):
    res = client.get("/UserHealthHistory?userID=1")

    assert res.status_code == 200
    
    assert res.json()

