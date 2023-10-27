from pydantic import BaseModel

class BaseHealth(BaseModel):
    entry: list['BaseHealthEntry']

class Health(BaseHealth):
    id: int
        
class BaseHealthEntry(BaseModel):
    userID: int
    dateStamp: str
    height: float
    weight: float
    fatPercentage: float
    musclePercentage: float
    waterPercentage: float

class HealthEntry(BaseHealthEntry):
    id: int
    
# class Height(BaseModel):
#     height: float
#     dateStamp: str

# class Weight(BaseModel):
#     weight: float
#     dateStamp: str

# class FatPercentage(BaseModel):
#     fatPercentage: float
#     dateStamp: str

# class MusclePercentage(BaseModel):
#     musclePercentage: float
#     dateStamp: str

# class WaterPercentage(BaseModel):
#     waterPercentage: float
#     dateStamp: str
    







