from fastapi import FastAPI
import json
import mysql.connector
from pprint import pprint

app = FastAPI()

database = mysql.connector.connect(
    host='krishusdata.mysql.database.azure.com',
    user='kmg',
    password='krissupersecretpassword0!',
    database='HealthService',
)

cursor = database.cursor()

@app.post("/insertHealth/")
def InsertHealthEntry(userID, dateStamp, height, weight, fatPercentage, musclePercentage, waterPercentage):
    if(userID == None or dateStamp == None):
        return
    
    if(height != None):
        cursor.execute(f"INSERT INTO heightLog VALUES(0, {userID}, '{dateStamp}', {height})")
        database.commit()
    
    if(weight != None):
        cursor.execute(f"INSERT INTO weightLog VALUES(0, {userID}, '{dateStamp}', {weight})")
        database.commit()

    if(fatPercentage != None):
        cursor.execute(f"INSERT INTO fatPercentageLog VALUES(0, {userID}, '{dateStamp}', {fatPercentage})")
        database.commit()
        
    if(musclePercentage != None):
        cursor.execute(f"INSERT INTO musclePercentageLog VALUES(0, {userID}, '{dateStamp}', {musclePercentage})")
        database.commit()
        
    if(waterPercentage != None):
        cursor.execute(f"INSERT INTO waterPercentageLog VALUES(0, {userID}, '{dateStamp}', {waterPercentage})")
        database.commit()


@app.post("/deleteHealth/")
def DeleteHealthEntry(userID, entryDateStamp, entryType, entryValue):
    if(userID == None or entryDateStamp == None or entryType == None or entryValue == None):
        return

    if(entryType == "height"):
        cursor.execute(f"DELETE FROM heightLog WHERE dateStamp='{entryDateStamp}' AND height={entryValue}")
        database.commit()
  
    elif(entryType == "weight"):
        cursor.execute(f"DELETE FROM weightLog WHERE dateStamp='{entryDateStamp}' AND weight={entryValue}")
        database.commit()
        
    elif(entryType == "fatPercentage"):
        cursor.execute(f"DELETE FROM fatPercentageLog WHERE dateStamp='{entryDateStamp}' AND fatPercentage={entryValue}")
        database.commit()
        
    elif(entryType == "musclePercentage"):
        cursor.execute(f"DELETE FROM musclePercentageLog WHERE dateStamp='{entryDateStamp}' AND musclePercentage={entryValue}")
        database.commit()
        
    elif(entryType == "waterPercentage"):
        cursor.execute(f"DELETE FROM waterPercentageLog WHERE dateStamp='{entryDateStamp}' AND waterPercentage={entryValue}")
        database.commit()
    
    else:
        print(f"There's an error with the entry type: {entryType}")


@app.get("/getHealth/")
def GetUsersLatestHealthEntry(userID):
    
    data = {
        "height": [],
        "weight": [],
        "fatPercentage": [],
        "musclePercentage": [],
        "waterPercentage": []
    }
    
    # HEIGHT
    cursor.execute(f"SELECT dateStamp, height FROM heightLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    heightResult = cursor.fetchone()
    dateStamp = heightResult[0]
    height = heightResult[1]
    data["height"].append({"dateStamp": f"{dateStamp}", "height": height})

    # WEIGHT
    cursor.execute(f"SELECT dateStamp, weight FROM weightLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    weightResult = cursor.fetchone()
    dateStamp = weightResult[0]
    weight = weightResult[1]
    data["weight"].append({"dateStamp": f"{dateStamp}", "weight": weight})

    # FAT
    cursor.execute(f"SELECT dateStamp, fatPercentage FROM fatPercentageLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    fatPercentageResult = cursor.fetchone()
    dateStamp = fatPercentageResult[0]
    fatPercentage = fatPercentageResult[1]
    data["fatPercentage"].append({"dateStamp": f"{dateStamp}", "fatPercentage": fatPercentage})
    
    # MUSCLE
    cursor.execute(f"SELECT dateStamp, musclePercentage FROM musclePercentageLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    musclePercentageResult = cursor.fetchone()
    dateStamp = musclePercentageResult[0]
    musclePercentage = musclePercentageResult[1]
    data["musclePercentage"].append({"dateStamp": f"{dateStamp}", "musclePercentage": musclePercentage})
    
    # WATER
    cursor.execute(f"SELECT dateStamp, waterPercentage FROM waterPercentageLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    waterPercentageResult = cursor.fetchone()
    dateStamp = waterPercentageResult[0]
    waterPercentage = waterPercentageResult[1]
    data["waterPercentage"].append({"dateStamp": f"{dateStamp}", "waterPercentage": waterPercentage})
    
    return data

@app.get("/UserHealthHistory")
def GetUsersHealthEntries(userID):

    data = {
        "height": [],
        "weight": [],
        "fatPercentage": [],
        "musclePercentage": [],
        "waterPercentage": []
    }

    cursor.execute(f"SELECT dateStamp, height FROM heightLog WHERE userID={userID} ORDER BY id DESC")
    for entry in cursor.fetchall():
        data["height"].append({"dateStamp": f"{entry[0]}", "height": entry[1]})

    cursor.execute(f"SELECT dateStamp, weight FROM weightLog WHERE userID={userID} ORDER BY id DESC")
    for entry in cursor.fetchall():
        data["weight"].append({"dateStamp": f"{entry[0]}", "weight": entry[1]})

    cursor.execute(f"SELECT dateStamp, fatPercentage FROM fatPercentageLog WHERE userID={userID} ORDER BY id DESC")
    for entry in cursor.fetchall():     
        data["fatPercentage"].append({"dateStamp": f"{entry[0]}", "fatPercentage": entry[1]})

    cursor.execute(f"SELECT dateStamp, musclePercentage FROM musclePercentageLog WHERE userID={userID} ORDER BY id DESC")
    for entry in cursor.fetchall():     
        data["musclePercentage"].append({"dateStamp": f"{entry[0]}", "musclePercentage": entry[1]})

    cursor.execute(f"SELECT dateStamp, waterPercentage FROM waterPercentageLog WHERE userID={userID} ORDER BY id DESC")
    for entry in cursor.fetchall():     
        data["waterPercentage"].append({"dateStamp": f"{entry[0]}", "waterPercentage": entry[1]})

    return data



# InsertHealthEntry(2, "2023-09-10 20:52:00", 172, 73, 18.3, 40, 32.5)

# latestEntry = GetUsersLatestHealthEntry(2)

# pprint(latestEntry)

# DeleteHealthEntry(2, "2023-09-10 20:52:00", "weight", 73)

# allEntries = GetUsersHealthEntries(1)
