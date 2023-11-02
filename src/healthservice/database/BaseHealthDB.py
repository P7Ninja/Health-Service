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
    
    def DeleteHealthEntry(self, userID: int, entryDateStamp: str, entryType: str, entryValue: float) -> None:
        return
    
    def GetUsersLatestHealthEntry(self, userID: int) -> None:
        return
    
    def GetUsersHealthEntries(self, userID: int) -> None:
        return




