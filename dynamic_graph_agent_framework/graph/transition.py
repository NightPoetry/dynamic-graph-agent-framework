from typing import Optional, Dict, Any

class TransitionCommand:
    def __init__(
        self,
        target: Any,
        update_global: Optional[Dict[str, Any]] = None,
        update_local: Optional[Dict[str, Any]] = None
    ):
        self.target = target
        self.update_global = update_global or {}
        self.update_local = update_local or {}
    
    def apply_updates(self, global_memory, local_memory=None):
        for key, value in self.update_global.items():
            global_memory.set(key, value)
        
        if local_memory:
            for key, value in self.update_local.items():
                local_memory.set(key, value)
    
    def __repr__(self) -> str:
        return f"TransitionCommand(target={self.target})"

END = "END"
