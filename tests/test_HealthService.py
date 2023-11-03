import pytest
import shutil
import json
import datetime
from pytest import FixtureRequest
from pathlib import Path
from fastapi import FastAPI
from fastapi.testclient import TestClient
from healthservice import HealthService, SQLHealthDB
from healthservice.database.health_schema import HealthEntry, BaseHealthEntry


@pytest.fixture
def db(request: FixtureRequest, tmp_path: Path):
    db_path = tmp_path / "db"
    db_path.mkdir()
    db_file = db_path / "db.sql"
    shutil.copyfile("./tests/test.db", db_file)
    db = SQLHealthDB({"DB_CONN": f"sqlite:///{db_file}"})
    db.startup()
    def tearddown():
        db.shutdown()

    request.addfinalizer(tearddown)
    return db

def test_InsertHealthEntry(db: SQLHealthDB):
    input = BaseHealthEntry(
        userID=2,
        dateStamp=datetime.datetime(2023, 11, 3, 12, 28, 18, 52000),
        height=170,
        weight=70,
        fatPercentage=20,
        musclePercentage=80,
        waterPercentage=60
    )
    db.InsertHealthEntry(input)
    db_health = db.GetUsersLatestHealthEntry(2)
    
    # this is a hack since the id is autoincremented
    health_entry = BaseHealthEntry(
                    userID=db_health.userID,
                    dateStamp=db_health.dateStamp,
                    height=db_health.height,
                    weight=db_health.weight,
                    fatPercentage=db_health.fatPercentage,
                    musclePercentage=db_health.musclePercentage,
                    waterPercentage=db_health.waterPercentage
                    )
    
    assert health_entry == input

def test_DeleteHealthEntry(db: SQLHealthDB):
    entry = db.GetUsersLatestHealthEntry(3)
    assert entry is not None
    db.DeleteHealthEntry(entry.id)
    next_entry = db.GetUsersLatestHealthEntry(3)
    assert next_entry.id is not entry.id

def test_GetUsersLatestHealthEntry(db: SQLHealthDB):
    
    health_entry = db.GetUsersLatestHealthEntry(0)

    assert isinstance(health_entry, HealthEntry)
    
    assert health_entry.userID == 0
    assert health_entry.dateStamp == datetime.datetime(2023, 11, 3, 12, 28, 18, 52000) #"2023-11-03T12:28:18.052000"
    assert health_entry.height == 170
    assert health_entry.weight == 70
    assert health_entry.fatPercentage == 20
    assert health_entry.musclePercentage == 80
    assert health_entry.waterPercentage == 60

    
def test_GetUsersHealthEntries(db: SQLHealthDB):
    health_entries = db.GetUsersHealthEntries(1)

    assert isinstance(health_entries, list)
    
    assert all(isinstance(entry, HealthEntry) for entry in health_entries)
    
    
    







