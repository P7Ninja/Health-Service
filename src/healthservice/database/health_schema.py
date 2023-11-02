from pydantic import BaseModel, validator, root_validator
from datetime import datetime
from typing import Optional

class BaseHealth(BaseModel):
    entry: list['BaseHealthEntry']

class Health(BaseHealth):
    id: int
        
class BaseHealthEntry(BaseModel):
    userID: int
    dateStamp: datetime
    height: Optional[float] = None
    weight: Optional[float] = None
    fatPercentage: Optional[float] = None
    musclePercentage:Optional[float] = None
    waterPercentage: Optional[float] = None
        
        

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
    







