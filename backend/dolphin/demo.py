#!/usr/bin/env python3
"""
Dolphin ByteDance Demo Script

This script demonstrates how to use the Dolphin ByteDance integration.
"""

import os
import asyncio
from dolphin.service import get_dolphin_service

async def demo_dolphin():
    """
    Demo function showing Dolphin ByteDance usage
    """
    print("🐬 Dolphin ByteDance Demo")
    print("=" * 40)
    
    # Check if API key is available
    api_key = os.getenv("DOLPHIN_API_KEY")
    if not api_key:
        print("❌ DOLPHIN_API_KEY not set")
        print("To use Dolphin ByteDance, set your API key:")
        print("export DOLPHIN_API_KEY='your-api-key-here'")
        print("\nDemo will run in simulation mode...")
        
        # Simulate response
        print("\n🤖 Simulated Chat Response:")
        print("User: Hello, how are you?")
        print("Dolphin: Hello! I'm doing well, thank you for asking. I'm here to help you with any questions or tasks you might have. How can I assist you today?")
        return
    
    try:
        # Initialize service
        service = get_dolphin_service()
        
        # Test chat
        print("\n🤖 Testing Dolphin Chat:")
        user_message = "Hello, how are you?"
        print(f"User: {user_message}")
        
        response = await service.chat(user_message)
        print(f"Dolphin: {response}")
        
        print("\n✅ Dolphin integration working successfully!")
        
    except Exception as e:
        print(f"\n❌ Error testing Dolphin: {e}")
        print("Make sure your API key is valid and you have internet connection.")

if __name__ == "__main__":
    asyncio.run(demo_dolphin())