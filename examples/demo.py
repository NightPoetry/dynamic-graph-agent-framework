import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dynamic_graph_agent_framework.ai_tools import AIConfig, OpenAIClient, SystemMessage, UserMessage, AIMessage, text_call, json_call, Context
from dynamic_graph_agent_framework.graph import Node, Graph, TransitionCommand, END

async def example_simple_graph():
    """简单图示例：展示基本的节点转移"""
    print("=== 示例1：简单图 ===\n")
    
    call_log = []
    
    def on_enter_start(node, graph):
        call_log.append(node.name)
        print(f"进入节点: {node.name}")
        graph.global_memory.set("counter", 1)
        return TransitionCommand(target="middle")
    
    def on_enter_middle(node, graph):
        call_log.append(node.name)
        print(f"进入节点: {node.name}")
        counter = graph.global_memory.get("counter", 0)
        graph.global_memory.set("counter", counter + 1)
        return TransitionCommand(target="end")
    
    def on_enter_end(node, graph):
        call_log.append(node.name)
        print(f"进入节点: {node.name}")
        print(f"最终计数器值: {graph.global_memory.get('counter')}")
        return TransitionCommand(target=END)
    
    start = Node("start", on_enter=on_enter_start)
    middle = Node("middle", on_enter=on_enter_middle)
    end = Node("end", on_enter=on_enter_end)
    
    graph = Graph(start)
    graph.link(start, middle)
    graph.link(middle, end)
    
    await graph.execute()
    print(f"执行路径: {' -> '.join(call_log)}\n")

async def example_ai_integration():
    """AI集成示例：在节点中使用AI工具"""
    print("=== 示例2：AI集成 ===\n")
    
    config = AIConfig.from_dict({
        "api_key": "sk-1ab795f0057743039e1f9b7b68d24913",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-flash",
        "temperature": 0.7,
        "streaming": True
    })
    
    client = OpenAIClient(config)
    
    async def on_enter_analyze(node, graph):
        print("进入节点: analyze")
        
        async with client:
            messages = [
                SystemMessage("你是一个简洁的分析助手，用一句话总结。"),
                UserMessage("Python是一种编程语言。")
            ]
            
            response = ""
            async for chunk in text_call(client, messages, stream=True):
                print(chunk, end="", flush=True)
                response += chunk
            print()
            
            graph.global_memory.set("summary", response)
            return TransitionCommand(target="process")
    
    async def on_enter_process(node, graph):
        print("\n进入节点: process")
        summary = graph.global_memory.get("summary", "")
        print(f"分析结果: {summary}")
        return TransitionCommand(target=END)
    
    analyze_node = Node("analyze", on_enter=on_enter_analyze)
    process_node = Node("process", on_enter=on_enter_process)
    
    graph = Graph(analyze_node)
    graph.link(analyze_node, process_node)
    
    await graph.execute()
    print()

async def example_context_usage():
    """上下文使用示例：展示Context对象的使用"""
    print("=== 示例3：上下文管理 ===\n")
    
    context = Context()
    
    context.append(SystemMessage("你是一个助手。"))
    context.append(UserMessage("你好"))
    context.append(AIMessage("你好！有什么可以帮助你的？"))
    context.append(UserMessage("介绍一下Python"))
    
    print(f"上下文消息数量: {len(context)}")
    print("最后3条消息:")
    for msg in context.get_last_n(3):
        print(f"  [{msg.role}]: {msg.content[:50]}...")
    
    print(f"\n转换为OpenAI格式:")
    messages = context.to_messages()
    for msg in messages:
        print(f"  {msg}\n")

async def example_json_call():
    """JSON调用示例：结构化数据提取"""
    print("=== 示例4：JSON调用 ===\n")
    
    config = AIConfig.from_dict({
        "api_key": "sk-1ab795f0057743039e1f9b7b68d24913",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-flash",
        "temperature": 0.1,
        "streaming": False
    })
    
    client = OpenAIClient(config)
    
    async with client:
        messages = [
            SystemMessage("你是一个数据生成助手。"),
            UserMessage("生成一个包含name、age、city的JSON对象。")
        ]
        
        result = await json_call(client, messages)
        print(f"生成的JSON数据: {result}\n")

async def example_parallel_branches():
    """并行分支示例：多分支同时执行"""
    print("=== 示例5：并行分支 ===\n")
    
    results = []
    
    def on_enter_start(node, graph):
        print("进入节点: start")
        return [
            TransitionCommand(target="branch_a"),
            TransitionCommand(target="branch_b"),
            TransitionCommand(target="branch_c")
        ]
    
    def on_enter_branch_a(node, graph):
        print("  执行分支 A")
        results.append("A")
        return TransitionCommand(target=END)
    
    def on_enter_branch_b(node, graph):
        print("  执行分支 B")
        results.append("B")
        return TransitionCommand(target=END)
    
    def on_enter_branch_c(node, graph):
        print("  执行分支 C")
        results.append("C")
        return TransitionCommand(target=END)
    
    start = Node("start", on_enter=on_enter_start)
    branch_a = Node("branch_a", on_enter=on_enter_branch_a)
    branch_b = Node("branch_b", on_enter=on_enter_branch_b)
    branch_c = Node("branch_c", on_enter=on_enter_branch_c)
    
    graph = Graph(start, parallel_execution=True)
    graph.link(start, branch_a)
    graph.link(start, branch_b)
    graph.link(start, branch_c)
    
    await graph.execute()
    print(f"执行结果: {', '.join(sorted(results))}\n")

async def example_dynamic_node_creation():
    """动态节点创建示例：运行时创建节点"""
    print("=== 示例6：动态节点创建 ===\n")
    
    def on_enter_root(node, graph):
        print("进入节点: root")
        
        new_node = Node("dynamic")
        
        def on_enter_dynamic(n, g):
            print("进入动态创建的节点")
            return TransitionCommand(target=END)
        
        new_node.set_on_enter(on_enter_dynamic)
        graph.add_node(new_node)
        graph.link(node, new_node)
        
        return TransitionCommand(target="dynamic")
    
    root = Node("root", on_enter=on_enter_root)
    graph = Graph(root)
    
    await graph.execute()
    print()

async def example_memory_management():
    """记忆管理示例：全局和局部记忆"""
    print("=== 示例7：记忆管理 ===\n")
    
    def on_enter_first(node, graph):
        print("进入节点: first")
        node.local_memory.set("local_data", "来自first节点")
        graph.global_memory.set("global_data", "全局数据")
        return TransitionCommand(target="second")
    
    def on_enter_second(node, graph):
        print("进入节点: second")
        print(f"  全局记忆: {graph.global_memory.to_dict()}")
        print(f"  局部记忆: {node.local_memory.to_dict()}")
        return TransitionCommand(target=END)
    
    first = Node("first", on_enter=on_enter_first)
    second = Node("second", on_enter=on_enter_second)
    
    graph = Graph(first)
    graph.link(first, second)
    
    await graph.execute()
    print()

async def main():
    await example_simple_graph()
    await example_ai_integration()
    await example_context_usage()
    await example_json_call()
    await example_parallel_branches()
    await example_dynamic_node_creation()
    await example_memory_management()
    print("所有示例执行完成！")

if __name__ == "__main__":
    asyncio.run(main())
