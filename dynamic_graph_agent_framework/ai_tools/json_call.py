import json
import re
from typing import Any, Dict, Optional, List
from .client import OpenAIClient
from .config import AIConfig
from .messages import BaseMessage

async def json_call(
    client: OpenAIClient,
    messages: List[BaseMessage],
    schema: Optional[Dict[str, Any]] = None,
    max_retries: Optional[int] = None
) -> Dict[str, Any]:
    config = client.config
    retries = max_retries if max_retries is not None else config.max_retries
    
    if schema:
        messages.append(BaseMessage(
            role="system",
            content=f"Please respond with valid JSON following this schema: {json.dumps(schema)}"
        ))
    
    for attempt in range(retries + 1):
        try:
            response_chunks = []
            async for chunk in client.chat(messages, stream=False, json_mode=True):
                response_chunks.append(chunk)
            
            response_data = response_chunks[0]
            content = response_data['choices'][0]['message']['content']
            
            parsed_json = _parse_and_fix_json(content)
            
            if parsed_json:
                return parsed_json
            elif attempt < retries:
                continue
            else:
                raise ValueError(f"Failed to parse JSON after {retries + 1} attempts")
        
        except Exception as e:
            if attempt < retries:
                await asyncio.sleep(1)
                continue
            else:
                raise e
    
    raise RuntimeError("Unexpected error in json_call")

def _parse_and_fix_json(content: str) -> Optional[Dict[str, Any]]:
    content = content.strip()
    
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    try:
        content = content.replace("'", '"')
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    try:
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    return None

import asyncio
