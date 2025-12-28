from typing import Any, Optional

class Memory:
    def __init__(self):
        self._data: dict = {}
    
    def set(self, key: str, value: Any):
        self._data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)
    
    def update(self, data: dict):
        self._data.update(data)
    
    def delete(self, key: str):
        if key in self._data:
            del self._data[key]
    
    def clear(self):
        self._data.clear()
    
    def to_dict(self) -> dict:
        return self._data.copy()
    
    def __contains__(self, key: str) -> bool:
        return key in self._data
    
    def __repr__(self) -> str:
        return f"Memory(keys={list(self._data.keys())})"
