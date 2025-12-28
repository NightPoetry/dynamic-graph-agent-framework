from typing import Optional, AsyncGenerator, List, Dict, Any
import aiohttp
import asyncio
from .config import AIConfig
from .messages import BaseMessage

class OpenAIClient:
    def __init__(self, config: AIConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
    
    def _convert_messages(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        return [msg.to_dict() for msg in messages]
    
    async def _make_request(
        self,
        messages: List[BaseMessage],
        stream: bool = False,
        json_mode: bool = False
    ) -> AsyncGenerator[str, None]:
        if not self.session:
            raise RuntimeError("Client session not initialized. Use async with statement.")
        
        url = f"{self.config.base_url}/chat/completions"
        headers = self._get_headers()
        
        payload = {
            "model": self.config.model,
            "messages": self._convert_messages(messages),
            "temperature": self.config.temperature,
            "stream": stream
        }
        
        if json_mode:
            payload["response_format"] = {"type": "json_object"}
        
        async with self.session.post(
            url,
            headers=headers,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"API request failed with status {response.status}: {error_text}")
            
            if stream:
                async for line in response.content:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        data = line_str[6:]
                        if data == '[DONE]':
                            break
                        yield data
            else:
                data = await response.json()
                yield data
    
    async def chat(
        self,
        messages: List[BaseMessage],
        stream: bool = False,
        json_mode: bool = False
    ) -> AsyncGenerator[str, None]:
        async for chunk in self._make_request(messages, stream, json_mode):
            yield chunk
