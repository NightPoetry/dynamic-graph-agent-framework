import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dynamic_graph_agent_framework.ai_tools import AIConfig, OpenAIClient, SystemMessage, UserMessage, text_call, json_call

async def test_ai_tools():
    config = AIConfig.from_dict({
        "api_key": "sk-1ab795f0057743039e1f9b7b68d24913",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-flash",
        "temperature": 0.1,
        "streaming": True,
        "max_retries": 3,
        "timeout": 60
    })
    
    async with OpenAIClient(config) as client:
        print("=== 测试文本调用（流式） ===")
        messages = [
            SystemMessage("你是一个友好的助手。"),
            UserMessage("你好，请介绍一下你自己。")
        ]
        
        response_text = ""
        async for chunk in text_call(client, messages, stream=True):
            print(chunk, end="", flush=True)
            response_text += chunk
        print("\n")
        
        print("=== 测试JSON调用 ===")
        json_messages = [
            SystemMessage("你是一个数据生成助手。"),
            UserMessage("请生成一个包含name、age、city的JSON对象，代表一个虚拟人物。")
        ]
        
        result = await json_call(client, json_messages)
        print(f"JSON结果: {result}\n")

if __name__ == "__main__":
    asyncio.run(test_ai_tools())
