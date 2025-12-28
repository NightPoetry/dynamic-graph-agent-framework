from typing import List, Dict, Any
from .messages import BaseMessage

class Context:
    def __init__(self):
        self.messages: List[BaseMessage] = []
    
    def append(self, message: BaseMessage):
        self.messages.append(message)
    
    def extend(self, messages: List[BaseMessage]):
        self.messages.extend(messages)
    
    def to_messages(self) -> List[Dict[str, str]]:
        return [msg.to_dict() for msg in self.messages]
    
    def get_last_n(self, n: int) -> List[BaseMessage]:
        return self.messages[-n:] if n > 0 else []
    
    def clear(self):
        self.messages.clear()
    
    def __len__(self) -> int:
        return len(self.messages)
    
    def __getitem__(self, index: int) -> BaseMessage:
        return self.messages[index]
    
    def __repr__(self) -> str:
        return f"Context(messages={len(self.messages)})"
