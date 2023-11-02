from fastapi import FastAPI, HTTPException, status
from .database import BaseHealthDB
from .database.health_schema import HealthEntry, BaseHealthEntry, Health, BaseHealth
from typing import Annotated


class HealthService:
    def __init__(self, app: FastAPI, database: BaseHealthDB, cfg: dict) -> None:
        self.__app = app
        self.__db = database
        self.__cfg = cfg
        
    def configure_database(self):
        @self.__app.on_event("startup")
        def startup():
            self.__db.startup()
        
        @self.__app.on_event("shutdown")
        def shutdown():
            self.__db.shutdown()
            
    def configure_routes(self):
        self.__app.add_api_route("/insertHealth", self.InsertHealthEntry, methods=["POST"])
        self.__app.add_api_route("/deleteHealth", self.DeleteHealthEntry, methods=["DELETE"])
        self.__app.add_api_route("/getHealth", self.GetUsersLatestHealthEntry, methods=["GET"])
        self.__app.add_api_route("/UserHealthHistory", self.GetUsersHealthEntries, methods=["GET"])
    
    async def InsertHealthEntry(self, health: BaseHealthEntry):
        self.__db.InsertHealthEntry(health)
        return {"success": True} 
    
    async def DeleteHealthEntry(self, 
                          id: int = 0, 
                          ):
        self.__db.DeleteHealthEntry(id)
        return {"success": True}
    
    async def GetUsersLatestHealthEntry(self, 
                                  userID: int = 0):
        return self.__db.GetUsersLatestHealthEntry(userID)
    
    async def GetUsersHealthEntries(self, 
                              userID: int = 0):
        return self.__db.GetUsersHealthEntries(userID)
    
    