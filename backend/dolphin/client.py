import asyncio
import httpx
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DolphinByteDanceClient:
    """
    Client for interacting with Dolphin ByteDance model
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://ark.cn-beijing.volces.com/api/v3"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient()
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def generate_response(self, 
                              messages: list, 
                              model: str = "ep-20241018143634-lwzsz",
                              max_tokens: int = 1000,
                              temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate a response using Dolphin ByteDance model
        
        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model endpoint ID
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Dictionary containing the response
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise
    
    async def stream_response(self, 
                            messages: list, 
                            model: str = "ep-20241018143634-lwzsz",
                            max_tokens: int = 1000,
                            temperature: float = 0.7):
        """
        Stream response from Dolphin ByteDance model
        
        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model endpoint ID
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Yields:
            Streaming response chunks
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True
        }
        
        try:
            async with self.client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30.0
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data.strip() == "[DONE]":
                            break
                        try:
                            import json
                            chunk = json.loads(data)
                            yield chunk
                        except json.JSONDecodeError:
                            continue
                            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

# Convenience function for simple usage
async def chat_with_dolphin(message: str, 
                          api_key: str,
                          conversation_history: Optional[list] = None) -> str:
    """
    Simple function to chat with Dolphin ByteDance
    
    Args:
        message: User message
        api_key: API key for authentication
        conversation_history: Previous conversation messages
        
    Returns:
        Model response as string
    """
    
    messages = conversation_history or []
    messages.append({"role": "user", "content": message})
    
    async with DolphinByteDanceClient(api_key=api_key) as client:
        response = await client.generate_response(messages)
        return response["choices"][0]["message"]["content"]