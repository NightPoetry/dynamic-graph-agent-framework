import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dynamic_graph_agent_framework.graph import Node, Graph, TransitionCommand, END, Memory

def test_graph_basic():
    print("=== 测试图框架基础功能 ===")
    
    call_log = []
    
    def on_enter_a(node, graph):
        call_log.append(f"Enter {node.name}")
        node.local_memory.set("data", "from_a")
        graph.global_memory.set("global_data", "from_a_global")
        return TransitionCommand(target="B", update_global={"step": 1})
    
    def on_enter_b(node, graph):
        call_log.append(f"Enter {node.name}")
        node.local_memory.set("data", "from_b")
        return TransitionCommand(target="C")
    
    def on_enter_c(node, graph):
        call_log.append(f"Enter {node.name}")
        return TransitionCommand(target=END)
    
    node_a = Node("A", on_enter=on_enter_a)
    node_b = Node("B", on_enter=on_enter_b)
    node_c = Node("C", on_enter=on_enter_c)
    
    graph = Graph(node_a, parallel_execution=False)
    graph.link(node_a, node_b)
    graph.link(node_b, node_c)
    
    asyncio.run(graph.execute())
    
    print(f"调用日志: {call_log}")
    print(f"全局记忆: {graph.global_memory.to_dict()}")
    print(f"节点A记忆: {node_a.local_memory.to_dict()}")
    print(f"节点B记忆: {node_b.local_memory.to_dict()}")
    
    assert call_log == ["Enter A", "Enter B", "Enter C"]
    assert graph.global_memory.get("step") == 1
    assert node_a.local_memory.get("data") == "from_a"
    assert node_b.local_memory.get("data") == "from_b"
    
    print("✓ 基础图框架测试通过\n")

def test_graph_parallel():
    print("=== 测试并行执行 ===")
    
    call_log = []
    
    def on_enter_a(node, graph):
        call_log.append(f"Enter {node.name}")
        return [
            TransitionCommand(target="B"),
            TransitionCommand(target="C")
        ]
    
    def on_enter_b(node, graph):
        call_log.append(f"Enter {node.name}")
        return TransitionCommand(target=END)
    
    def on_enter_c(node, graph):
        call_log.append(f"Enter {node.name}")
        return TransitionCommand(target=END)
    
    node_a = Node("A", on_enter=on_enter_a)
    node_b = Node("B", on_enter=on_enter_b)
    node_c = Node("C", on_enter=on_enter_c)
    
    graph = Graph(node_a, parallel_execution=True)
    graph.link(node_a, node_b)
    graph.link(node_a, node_c)
    
    asyncio.run(graph.execute())
    
    print(f"调用日志: {call_log}")
    assert "Enter A" in call_log
    assert "Enter B" in call_log
    assert "Enter C" in call_log
    
    print("✓ 并行执行测试通过\n")

def test_node_dynamic_binding():
    print("=== 测试动态绑定 ===")
    
    call_log = []
    
    def on_enter_x(node, graph):
        call_log.append(f"Enter {node.name}")
        return TransitionCommand(target=END)
    
    node_x = Node("X")
    node_x.set_on_enter(on_enter_x)
    
    graph = Graph(node_x)
    
    asyncio.run(graph.execute())
    
    print(f"调用日志: {call_log}")
    assert call_log == ["Enter X"]
    
    print("✓ 动态绑定测试通过\n")

if __name__ == "__main__":
    test_graph_basic()
    test_graph_parallel()
    test_node_dynamic_binding()
    print("所有图框架测试通过！")
