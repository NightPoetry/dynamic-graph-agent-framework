from typing import Callable, Optional, Any, Coroutine
import uuid
from .memory import Memory

class Node:
    _node_counter = 0
    
    def __init__(self, name: str, on_enter: Optional[Callable] = None, on_exit: Optional[Callable] = None):
        self.node_id = Node._node_counter
        Node._node_counter += 1
        self.name = name
        self.local_memory = Memory()
        self.on_enter = on_enter
        self.on_exit = on_exit
        self._links: dict = {}
    
    def link(self, target_node: 'Node', link_name: Optional[str] = None):
        if link_name is None:
            link_name = target_node.name
        self._links[link_name] = target_node
    
    def get_linked_node(self, name_or_id: Any) -> Optional['Node']:
        if isinstance(name_or_id, int):
            for node in self._links.values():
                if node.node_id == name_or_id:
                    return node
        else:
            return self._links.get(name_or_id)
        return None
    
    def set_on_enter(self, callback: Callable):
        self.on_enter = callback
    
    def set_on_exit(self, callback: Callable):
        self.on_exit = callback
    
    async def enter(self, graph: 'Graph'):
        if self.on_enter:
            result = self.on_enter(self, graph)
            if isinstance(result, Coroutine):
                result = await result
            return result
        return None
    
    async def exit(self, graph: 'Graph'):
        if self.on_exit:
            result = self.on_exit(self, graph)
            if isinstance(result, Coroutine):
                result = await result
            return result
        return None
    
    def __repr__(self) -> str:
        return f"Node(id={self.node_id}, name='{self.name}')"
