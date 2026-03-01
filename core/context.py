import pandas as pd
from typing import Dict, Any, List

class ProfileCoreContext:
    """
    Stores data and logs throughout the analysis pipeline.
    """
    def __init__(self, workspace_dir: str = "workspace"):
        self.workspace_dir = workspace_dir
        self.data: Dict[str, pd.DataFrame] = {}
        self.logs: List[str] = []
        
    def set_data(self, key: str, df: pd.DataFrame):
        self.data[key] = df
        
    def get_data(self, key: str) -> pd.DataFrame:
        return self.data.get(key)
    
    def add_log(self, message: str):
        self.logs.append(message)
        print(message)
    
    def get_logs(self) -> List[str]:
        return self.logs
