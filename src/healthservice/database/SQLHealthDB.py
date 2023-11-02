from .health_schema import HealthEntry, BaseHealthEntry, Health, BaseHealth
from .BaseHealthDB import BaseHealthDB
from sqlalchemy import create_engine, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, session
from .model import sql as model
from .factory import health_from_schema, health_from_sql_model
from fastapi import HTTPException, status

class SQLHealthDB(BaseHealthDB):
    
    def __init__(self, cfg: dict) -> None:
        super().__init__(cfg)
        
    def startup(self, connect_args: dict=dict()):
        self.__engine = create_engine(self.cfg["DB_CONN"], connect_args=connect_args)
        self.__local = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        self.__db = self.__local()
        model.Base.metadata.create_all(self.__engine)

    def shutdown(self):
        session.close_all_sessions()
        self.__engine.dispose()
    
    
    def check_optional_fields(cls, health : BaseHealthEntry):
        if not [x for x in (health.height, health.weight, health.fatPercentage, health.musclePercentage, health.waterPercentage) if x is not None]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one of the optional fields must have a value")
    
    def InsertHealthEntry(self, healthEntry: BaseHealthEntry):   
        try: 
            self.check_optional_fields(healthEntry)
            db_health = health_from_schema(self.__db, healthEntry)
        except SQLAlchemyError as e:
            self.__db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return db_health
        

    def DeleteHealthEntry(self, id):        
        if(id == None):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request - No ID provided")

        health = self.__db.query(model.Health).filter(model.Health.id == id).first()
            
        try:
            if health is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found - No entry with that ID exists")
            self.__db.delete(health)
            self.__db.commit()
        except SQLAlchemyError as e:
            self.__db.rollback()
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
        return 

    def GetUsersLatestHealthEntry(self, userID):
        
        health = self.__db.query(model.Health).filter(model.Health.userID == userID).first()
        
        if health == None: # might not be reached
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request - User not found or no entries exist for the user")
        
        db_health = health_from_sql_model(health)
        self.check_optional_fields(db_health)
        return db_health

    def GetUsersHealthEntries(self, userID):
        healthList = []
        health = self.__db.query(model.Health).filter(model.Health.userID == userID).all()
        
        if health == None: # might not be reached
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request - User not found or no entries exist for the user")
        
        for h in health:
            healthList.append(health_from_sql_model(h))
            
        return healthList

        
    