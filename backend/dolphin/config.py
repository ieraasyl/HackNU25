from pydantic_settings import BaseSettings
from typing import Optional, Literal
from pathlib import Path
import os

class DolphinConfig(BaseSettings):
    """Configuration for Local Dolphin setup - No API keys needed!"""
    
    # Provider Configuration - Default to local (free!)
    provider: Literal["local", "bytedance", "replicate", "huggingface"] = "local"
    api_key: Optional[str] = None  # Not needed for local!
    
    # Local Dolphin Configuration
    local_model_path: str = str(Path.home() / "dolphin_models")
    local_model_name: str = "dolphin-2.5-mixtral-8x7b"  # Or any Dolphin variant
    local_device: str = "auto"  # auto, cpu, cuda, mps (for Mac)
    local_max_memory: Optional[str] = "20GB"  # Adjust for your Mac's RAM
    
    # Alternative: Use Ollama (easier local setup)
    use_ollama: bool = True  # Simpler local setup
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "dolphin-mistral"  # Available in Ollama
    
    # Cloud providers (if you change your mind later)
    bytedance_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    replicate_base_url: str = "https://api.replicate.com/v1"
    huggingface_base_url: str = "https://api-inference.huggingface.co/models"
    
    # Model Parameters
    max_tokens: int = 1000
    temperature: float = 0.7
    top_p: float = 0.95
    
    # Request Configuration
    timeout: float = 120.0  # Longer for local processing
    max_retries: int = 3
    
    @property
    def base_url(self) -> str:
        """Get base URL based on provider"""
        if self.provider == "local":
            return self.ollama_base_url if self.use_ollama else "local"
        elif self.provider == "bytedance":
            return self.bytedance_base_url
        elif self.provider == "replicate":
            return self.replicate_base_url
        elif self.provider == "huggingface":
            return self.huggingface_base_url
        else:
            return "http://localhost:11434"
    
    @property 
    def model_endpoint(self) -> str:
        """Get model endpoint based on provider"""
        if self.provider == "local":
            return self.ollama_model if self.use_ollama else self.local_model_name
        else:
            return f"{self.provider}-model"
    
    @property
    def requires_api_key(self) -> bool:
        """Check if current provider requires API key"""
        return self.provider in ["bytedance", "replicate", "huggingface"]
    
    class Config:
        env_prefix = "DOLPHIN_"
        env_file = ".env"

# Global configuration instance
dolphin_config = DolphinConfig()