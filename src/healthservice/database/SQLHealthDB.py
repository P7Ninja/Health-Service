from .health_schema import HealthEntry, BaseHealthEntry, Health, BaseHealth
from .BaseHealthDB import BaseHealthDB
from sqlalchemy import create_engine, func, or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, session
from .model import sql as model
from .factory import health_from_schema, health_from_sql_model

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
    
        
    def InsertHealthEntry(self, healthEntry: HealthEntry):
        if(healthEntry.dateStamp == None):
            return 
        
        try: 
            db_health = health_from_schema(self.__db, healthEntry)
        except SQLAlchemyError as e:
            self.__db.rollback()
            return e
        return db_health
        

    def DeleteHealthEntry(self, id):        
        if(id == None):
            return

        health = self.__db.query(model.Health).filter(model.Health.id == id).first()
            
        try:
            if health is None:
                return False
            self.__db.delete(health)
            self.__db.commit()
        except SQLAlchemyError as e:
            self.__db.rollback()
            return False
        return True

    def GetUsersLatestHealthEntry(self, userID):
        
        health = self.__db.query(model.Health).filter(model.Health.userID == userID).first()
        return health_from_sql_model(health)   

    def GetUsersHealthEntries(self, userID):
        healthList = []
        health = self.__db.query(model.Health).filter(model.Health.userID == userID).all()
        for h in health:
            healthList.append(health_from_sql_model(h))
        return healthList

        
    