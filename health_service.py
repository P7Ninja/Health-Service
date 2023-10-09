from fastapi import FastAPI
import json
import mysql.connector

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
    if(height != None):
        cursor.execute(f"INSERT INTO heightLog VALUES({userID}, '{dateStamp}', {height})")
        database.commit()
    
    if(weight != None):
        cursor.execute(f"INSERT INTO weight VALUES({userID}, '{dateStamp}', {weight})")
        database.commit()

    if(fatPercentage != None | musclePercentage != None | waterPercentage != None):
        cursor.execute(f"INSERT INTO bodyComposition VALUES({userID}, '{dateStamp}', {fatPercentage}, {musclePercentage}, {waterPercentage})")
        database.commit()



def UpdateHealthEntry(userID, weight, height, fatPercentage, musclePercentage, waterPercentage):
    print(">_<")


@app.get("/getHealth/")
def GetLatestHealthEntry(userID):
    cursor.execute(f"SELECT height FROM heightLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    heightResult = cursor.fetchone()
    height = heightResult[0]

    cursor.execute(f"SELECT weight FROM weightLog WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    weightResult = cursor.fetchone()
    weight = weightResult[0]

    cursor.execute(f"SELECT fatPercentage, musclePercentage, waterPercentage FROM bodyComposition WHERE userID={userID} ORDER BY id DESC LIMIT 0, 1")
    bodyCompositionResult = cursor.fetchone()
    fatPercentage = bodyCompositionResult[0]
    musclePercentage = bodyCompositionResult[1]
    waterPercentage = bodyCompositionResult[2]

    result = f'{{"userid": {userID}, "height": {height}, "weight": {weight}, "fatPercentage": {fatPercentage}, "musclePercentage": {musclePercentage}, "waterPercentage": {waterPercentage}}}'

    jsonFile = json.loads(result)
    return jsonFile

@app.get("/UserHealthHistory")
def GetAllUserHealthEntries(userID):

    cursor.execute(f"SELECT dateStamp, height FROM heightLog WHERE userID={userID} ORDER BY id DESC")

    index = 1
    allUserHeightEntries = ""
    for entry in cursor.fetchall():
        dateStamp = entry[0]
        height = entry[1]
        allUserHeightEntries += f'"entry{index}": {{"dateStamp": "{dateStamp}", "height": {height}}},'
        index += 1
    allUserHeightEntries = allUserHeightEntries[:-1]

    cursor.execute(f"SELECT dateStamp, weight FROM weightLog WHERE userID={userID} ORDER BY id DESC")
    index = 1
    allUserWeightEntries = ""
    for entry in cursor.fetchall():
        dateStamp = entry[0]
        weight = entry[1]
        allUserWeightEntries += f'"entry{index}": {{"dateStamp": "{dateStamp}", "weight": {weight}}},'
        index += 1
    allUserWeightEntries = allUserWeightEntries[:-1]

    # cursor.execute(f"SELECT dateStamp, fatPercentage, musclePercentage, waterPercentage FROM bodyComposition WHERE userID={userID} ORDER BY id DESC")
    # index = 1
    # allUserBodyCompositionEntries = ""
    # for entry in cursor.fetchall():
    #     dateStamp = entry[0]
    #     fatPercentage = entry[1]
    #     musclePercentage = entry[2]
    #     waterPercentage = entry[3]
    #     allUserBodyCompositionEntries += f'"entry{index}": {{"dateStamp": "{dateStamp}", "fatPercentage": {fatPercentage}, "musclePercentage": {musclePercentage}, "waterPercentage": {waterPercentage}}},'
    #     index += 1
    # allUserBodyCompositionEntries = allUserBodyCompositionEntries[:-1]

    cursor.execute(f"SELECT dateStamp, fatPercentage FROM fatPercentageLog WHERE userID={userID} ORDER BY id DESC")
    index = 1
    allUserFatPercentageEntries = ""
    for entry in cursor.fetchall():     
        dateStamp = entry[0]
        fatPercentage = entry[1]
        allUserFatPercentageEntries += f'"entry{index}": {{"dateStamp": "{dateStamp}", "fatPercentage": {fatPercentage}}},'
        index += 1
    allUserFatPercentageEntries = allUserFatPercentageEntries[:-1]

    cursor.execute(f"SELECT dateStamp, musclePercentage FROM musclePercentageLog WHERE userID={userID} ORDER BY id DESC")
    index = 1
    allUserMusclePercentageEntries = ""
    for entry in cursor.fetchall():     
        dateStamp = entry[0]
        musclePercentage = entry[1]
        allUserMusclePercentageEntries += f'"entry{index}": {{"dateStamp": "{dateStamp}", "musclePercentage": {musclePercentage}}},'
        index += 1
    allUserMusclePercentageEntries = allUserMusclePercentageEntries[:-1]

    cursor.execute(f"SELECT dateStamp, waterPercentage FROM waterPercentageLog WHERE userID={userID} ORDER BY id DESC")
    index = 1
    allUserWaterPercentageEntries = ""
    for entry in cursor.fetchall():     
        dateStamp = entry[0]
        waterPercentage = entry[1]
        allUserFatPercentageEntries += f'"entry{index}": {{"dateStamp": "{dateStamp}", "waterPercentage": {waterPercentage}}},'
        index += 1
    allUserWaterPercentageEntries = allUserWaterPercentageEntries[:-1]

    result = f'{{"height": {{{allUserHeightEntries}}}, "weight": {{{allUserWeightEntries}}}, "fatPercentage": {{{allUserFatPercentageEntries}}}, "musclePercentage": {{{allUserMusclePercentageEntries}}}, "waterPercentage": {{{allUserWaterPercentageEntries}}}}}'
    jsonFile = json.loads(result)

    with open('test.json', 'w') as f:
        json.dump(jsonFile, f)
    return jsonFile


# InsertHealthEntry(2)
# GetLatestHealthEntry(1)
GetAllUserHealthEntries(1)