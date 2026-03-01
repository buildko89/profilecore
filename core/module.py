from profilecore.core.context import ProfileCoreContext

class AnalysisModule:
    """
    Base class for all analysis modules.
    """
    def __init__(self, context: ProfileCoreContext):
        self.context = context
        
    def log(self, message: str):
        self.context.add_log(f"[{self.__class__.__name__}] {message}")
