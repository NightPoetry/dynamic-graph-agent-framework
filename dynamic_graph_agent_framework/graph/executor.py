from typing import List, Optional, Any
import asyncio
from .node import Node
from .transition import TransitionCommand, END

class Executor:
    def __init__(self, graph, parallel_execution: bool = False):
        self.graph = graph
        self.parallel_execution = parallel_execution
    
    async def run(self, entry_node: Node):
        queue = [(entry_node, None)]
        
        while queue:
            current_batch = queue
            queue = []
            
            if self.parallel_execution:
                await self._run_parallel(current_batch, queue)
            else:
                await self._run_sequential(current_batch, queue)
    
    async def _run_sequential(self, current_batch: List, queue: List):
        for node, source_node in current_batch:
            transitions = await self._execute_node(node, source_node)
            if transitions:
                for transition in transitions:
                    await self._process_transition(transition, node, queue)
    
    async def _run_parallel(self, current_batch: List, queue: List):
        tasks = []
        for node, source_node in current_batch:
            tasks.append(self._execute_node(node, source_node))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result, (node, source_node) in zip(results, current_batch):
            if isinstance(result, Exception):
                print(f"Error executing node {node}: {result}")
                continue
            
            if result:
                for transition in result:
                    await self._process_transition(transition, node, queue)
    
    async def _execute_node(self, node: Node, source_node: Optional[Node]) -> Optional[List[TransitionCommand]]:
        try:
            result = await node.enter(self.graph)
            
            if isinstance(result, TransitionCommand):
                result = [result]
            elif result is None:
                result = []
            
            await node.exit(self.graph)
            
            return result
        except Exception as e:
            print(f"Error in node {node.name}: {e}")
            return []
    
    async def _process_transition(self, transition: TransitionCommand, current_node: Node, queue: List):
        transition.apply_updates(self.graph.global_memory, current_node.local_memory)
        
        if transition.target == END:
            return
        
        target_node = None
        if isinstance(transition.target, int):
            target_node = self.graph.get_node_by_id(transition.target)
        elif isinstance(transition.target, str):
            target_node = current_node.get_linked_node(transition.target)
            if not target_node:
                target_node = self.graph.get_node_by_name(transition.target)
        elif isinstance(transition.target, Node):
            target_node = transition.target
        
        if target_node:
            queue.append((target_node, current_node))
        else:
            print(f"Warning: Target node {transition.target} not found")
