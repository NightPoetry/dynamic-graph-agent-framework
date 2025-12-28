from typing import Optional, List, Any
from .node import Node
from .memory import Memory
from .transition import TransitionCommand, END
from .executor import Executor

class Graph:
    def __init__(self, entry_node: Node, parallel_execution: bool = False):
        self.entry_node = entry_node
        self.global_memory = Memory()
        self.nodes: List[Node] = [entry_node]
        self.parallel_execution = parallel_execution
    
    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.append(node)
    
    def link(self, source: Node, target: Node, link_name: Optional[str] = None):
        source.link(target, link_name)
        if target not in self.nodes:
            self.add_node(target)
    
    def get_node_by_id(self, node_id: int) -> Optional[Node]:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
    
    def get_node_by_name(self, name: str) -> Optional[Node]:
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    async def execute(self, initial_context: Optional[dict] = None):
        if initial_context:
            for key, value in initial_context.items():
                self.global_memory.set(key, value)
        
        executor = Executor(self, self.parallel_execution)
        await executor.run(self.entry_node)
