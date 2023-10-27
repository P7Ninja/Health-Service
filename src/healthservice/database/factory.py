
from .model import sql as model
from .health_schema import HealthEntry, BaseHealthEntry, Health, BaseHealth
from sqlalchemy.orm import Session

def health_from_schema(session : Session, health: BaseHealthEntry):
    db_health = model.Health(
        userID=health.userID,
        dateStamp=health.dateStamp,
        height=health.height,
        weight=health.weight,
        fatPercentage=health.fatPercentage,
        musclePercentage=health.musclePercentage,
        waterPercentage=health.waterPercentage
    )
    
    session.add(db_health)
    session.commit()
    session.refresh(db_health)
    return db_health
    
def health_from_sql_model(health: model.Health):
    return HealthEntry(
        id=health.id,
        userID=health.userID,
        dateStamp=health.dateStamp,
        height=health.height,
        weight=health.weight,
        fatPercentage=health.fatPercentage,
        musclePercentage=health.musclePercentage,
        waterPercentage=health.waterPercentage
    )
