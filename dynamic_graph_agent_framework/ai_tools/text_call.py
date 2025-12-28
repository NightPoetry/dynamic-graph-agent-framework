from typing import AsyncGenerator, List
from .client import OpenAIClient
from .messages import BaseMessage

async def text_call(
    client: OpenAIClient,
    messages: List[BaseMessage],
    stream: bool = True
) -> AsyncGenerator[str, None]:
    async for chunk in client.chat(messages, stream=stream, json_mode=False):
        if stream:
            try:
                data = json.loads(chunk)
                if 'choices' in data and len(data['choices']) > 0:
                    delta = data['choices'][0].get('delta', {})
                    if 'content' in delta:
                        yield delta['content']
            except (json.JSONDecodeError, KeyError):
                continue
        else:
            data = chunk
            if 'choices' in data and len(data['choices']) > 0:
                yield data['choices'][0]['message']['content']

import json
