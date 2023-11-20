from .health_schema import HealthEntry

class BaseHealthDB:
    def __init__(self, cfg: dict) -> None:
            self.cfg = cfg
            
    def startup(self):
            return
        
    def shutdown(self):
        return

    
    def InsertHealthEntry(self, healthEntry: HealthEntry) -> None:
        return
    
    def DeleteHealthEntry(self, id: int, userID: int) -> None:
        return
    
    def GetUsersLatestHealthEntry(self, userID: int) -> HealthEntry:
        return
    
    def GetUsersHealthEntries(self, userID: int) -> list[HealthEntry]:
        return




