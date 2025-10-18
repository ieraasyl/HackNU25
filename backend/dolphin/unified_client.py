import asyncio
import httpx
import json
import base64
from typing import Optional, Dict, Any, List, AsyncGenerator
import logging
from .config import dolphin_config

logger = logging.getLogger(__name__)

class UnifiedDolphinClient:
    """
    Unified client for interacting with Dolphin models across different providers
    """
    
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None):
        self.api_key = api_key or dolphin_config.api_key
        self.provider = provider or dolphin_config.provider
        self.client = httpx.AsyncClient(timeout=dolphin_config.timeout)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def generate_response(self, 
                              messages: List[Dict[str, str]], 
                              max_tokens: int = None,
                              temperature: float = None) -> Dict[str, Any]:
        """
        Generate a response using the configured provider
        
        Args:
            messages: List of message objects with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            
        Returns:
            Dictionary containing the response
        """
        
        max_tokens = max_tokens or dolphin_config.max_tokens
        temperature = temperature or dolphin_config.temperature
        
        if self.provider == "bytedance":
            return await self._generate_bytedance(messages, max_tokens, temperature)
        elif self.provider == "replicate":
            return await self._generate_replicate(messages, max_tokens, temperature)
        elif self.provider == "huggingface":
            return await self._generate_huggingface(messages, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def _generate_bytedance(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Generate response using ByteDance API"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": dolphin_config.model_endpoint,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": dolphin_config.top_p
        }
        
        try:
            response = await self.client.post(
                f"{dolphin_config.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                return {
                    "response": data["choices"][0]["message"]["content"],
                    "usage": data.get("usage", {}),
                    "model": data.get("model", "unknown"),
                    "provider": "bytedance"
                }
            else:
                raise ValueError("No choices in response")
                
        except httpx.HTTPStatusError as e:
            logger.error(f"ByteDance API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"ByteDance API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"ByteDance request failed: {e}")
            raise
    
    async def _generate_replicate(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Generate response using Replicate API"""
        
        if not self.api_key:
            raise ValueError("API key required for Replicate")
        
        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert messages to prompt format for Replicate
        prompt = self._messages_to_prompt(messages)
        
        payload = {
            "version": "latest",  # You'd need to get the actual version ID
            "input": {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        }
        
        try:
            # Create prediction
            response = await self.client.post(
                f"{dolphin_config.base_url}/predictions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            prediction_data = response.json()
            prediction_id = prediction_data["id"]
            
            # Poll for completion
            while True:
                check_response = await self.client.get(
                    f"{dolphin_config.base_url}/predictions/{prediction_id}",
                    headers=headers
                )
                check_data = check_response.json()
                
                if check_data["status"] == "succeeded":
                    output = check_data.get("output", "")
                    if isinstance(output, list):
                        output = "".join(output)
                    
                    return {
                        "response": output,
                        "usage": {"total_tokens": len(output.split())},  # Approximate
                        "model": dolphin_config.model_endpoint,
                        "provider": "replicate"
                    }
                elif check_data["status"] == "failed":
                    raise Exception(f"Replicate prediction failed: {check_data.get('error', 'Unknown error')}")
                
                # Wait before polling again
                await asyncio.sleep(1)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Replicate API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Replicate API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Replicate request failed: {e}")
            raise
    
    async def _generate_huggingface(self, messages: List[Dict[str, str]], max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Generate response using Hugging Face Inference API"""
        
        if not self.api_key:
            raise ValueError("API key required for Hugging Face")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Convert messages to prompt
        prompt = self._messages_to_prompt(messages)
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }
        
        try:
            response = await self.client.post(
                f"{dolphin_config.base_url}/{dolphin_config.model_endpoint}",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different response formats
            if isinstance(data, list) and len(data) > 0:
                generated_text = data[0].get("generated_text", "")
            elif isinstance(data, dict):
                generated_text = data.get("generated_text", "")
            else:
                generated_text = str(data)
            
            return {
                "response": generated_text,
                "usage": {"total_tokens": len(generated_text.split())},  # Approximate
                "model": dolphin_config.model_endpoint,
                "provider": "huggingface"
            }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Hugging Face API error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Hugging Face API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Hugging Face request failed: {e}")
            raise
    
    def _messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """Convert chat messages to a single prompt string"""
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)
    
    async def stream_response(self, 
                            messages: List[Dict[str, str]], 
                            max_tokens: int = None,
                            temperature: float = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream response (fallback to non-streaming for now)
        """
        # For now, just return the full response as a single chunk
        # In a real implementation, you'd handle streaming per provider
        try:
            result = await self.generate_response(messages, max_tokens, temperature)
            yield {
                "choices": [{
                    "delta": {
                        "content": result["response"]
                    }
                }]
            }
        except Exception as e:
            yield {
                "error": str(e)
            }

# For backward compatibility
DolphinByteDanceClient = UnifiedDolphinClient