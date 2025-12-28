from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Optional
import json

class BaseMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

@dataclass
class SystemMessage:
    content: str
    role: str = field(default="system", init=False)
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

@dataclass
class UserMessage:
    content: str
    role: str = field(default="user", init=False)
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

@dataclass
class AIMessage:
    content: str
    role: str = field(default="assistant", init=False)
    
    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

@dataclass
class ToolMessage:
    content: str
    tool_call_id: Optional[str] = None
    role: str = field(default="tool", init=False)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role, "content": self.content}
        if self.tool_call_id is not None:
            result["tool_call_id"] = self.tool_call_id
        return result
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

class CustomMessage(BaseMessage):
    def __init__(self, role: str, content: str, **kwargs):
        super().__init__(role=role, content=content)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role, "content": self.content}
        for key, value in self.__dict__.items():
            if key not in ['role', 'content']:
                result[key] = value
        return result
