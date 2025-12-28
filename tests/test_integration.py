import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dynamic_graph_agent_framework.ai_tools import AIConfig, OpenAIClient, SystemMessage, UserMessage, text_call, Context
from dynamic_graph_agent_framework.graph import Node, Graph, TransitionCommand, END

async def test_integration():
    print("=== 集成测试：AI工具 + 图框架 ===")
    
    config = AIConfig.from_dict({
        "api_key": "sk-1ab795f0057743039e1f9b7b68d24913",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-flash",
        "temperature": 0.1,
        "streaming": True,
        "max_retries": 3,
        "timeout": 60
    })
    
    client = OpenAIClient(config)
    
    async def on_enter_start(node, graph):
        print(f"进入节点: {node.name}")
        
        async with client:
            messages = [
                SystemMessage("你是一个任务分析助手。"),
                UserMessage("分析一下：用户想要创建一个智能体框架。")
            ]
            
            response = ""
            async for chunk in text_call(client, messages, stream=True):
                print(chunk, end="", flush=True)
                response += chunk
            print()
            
            graph.global_memory.set("analysis", response)
            return TransitionCommand(target="process", update_global={"status": "analyzed"})
    
    async def on_enter_process(node, graph):
        print(f"\n进入节点: {node.name}")
        analysis = graph.global_memory.get("analysis", "")
        print(f"分析结果长度: {len(analysis)} 字符")
        return TransitionCommand(target=END)
    
    start_node = Node("start", on_enter=on_enter_start)
    process_node = Node("process", on_enter=on_enter_process)
    
    graph = Graph(start_node, parallel_execution=False)
    graph.link(start_node, process_node)
    
    await graph.execute()
    
    print("\n✓ 集成测试通过")

async def test_context_with_graph():
    print("\n=== 测试上下文与图框架结合 ===")
    
    context = Context()
    context.append(SystemMessage("系统提示"))
    context.append(UserMessage("用户消息"))
    
    print(f"上下文消息数: {len(context)}")
    print(f"上下文内容: {context.to_messages()}")
    
    print("✓ 上下文测试通过")

if __name__ == "__main__":
    asyncio.run(test_integration())
    asyncio.run(test_context_with_graph())
    print("\n所有集成测试通过！")
