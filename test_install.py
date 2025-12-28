import asyncio
from dynamic_graph_agent_framework import Node, Graph, TransitionCommand, END

async def test_import():
    print("测试导入agent_framework包...")
    
    call_log = []
    
    def on_enter_start(node, graph):
        call_log.append(node.name)
        print(f"进入节点: {node.name}")
        return TransitionCommand(target="end")
    
    def on_enter_end(node, graph):
        call_log.append(node.name)
        print(f"进入节点: {node.name}")
        return TransitionCommand(target=END)
    
    start = Node("start", on_enter=on_enter_start)
    end = Node("end", on_enter=on_enter_end)
    
    graph = Graph(start)
    graph.link(start, end)
    
    await graph.execute()
    
    print(f"\n执行路径: {' -> '.join(call_log)}")
    print("✓ 导入测试通过！")

if __name__ == "__main__":
    asyncio.run(test_import())
