#!/usr/bin/env python3
"""
Interactive Dolphin ByteDance Client

This script provides multiple ways to interact with the Dolphin integration.
"""

import os
import asyncio
import httpx
from dolphin.service import get_dolphin_service

async def test_api_endpoints():
    """Test the API endpoints directly"""
    print("🌐 Testing API Endpoints...")
    
    try:
        async with httpx.AsyncClient() as client:
            # Test root endpoint
            response = await client.get("http://127.0.0.1:8001/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint: {data['message']}")
                print(f"📋 Available endpoints:")
                for name, url in data.get('endpoints', {}).items():
                    print(f"   • {name}: {url}")
            
            # Test health endpoint
            response = await client.get("http://127.0.0.1:8001/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check: {data['status']}")
            
            # Test Dolphin health
            response = await client.get("http://127.0.0.1:8001/api/v1/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Dolphin service: {data['status']}")
                
    except Exception as e:
        print(f"❌ Could not connect to server: {e}")
        print("💡 Make sure the server is running with:")
        print("   PYTHONPATH=/path/to/backend python -m uvicorn dolphin_server:app --port 8001")

async def test_chat_api():
    """Test the chat API endpoint"""
    print("\n💬 Testing Chat API...")
    
    try:
        async with httpx.AsyncClient() as client:
            chat_data = {
                "message": "Hello, how are you?",
                "temperature": 0.7,
                "max_tokens": 100
            }
            
            response = await client.post(
                "http://127.0.0.1:8001/api/v1/chat",
                json=chat_data,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Dolphin Response: {data['response']}")
                print(f"📊 Tokens used: {data.get('usage', {}).get('total_tokens', 'N/A')}")
            else:
                print(f"❌ Chat API error: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Chat API test failed: {e}")

async def test_direct_service():
    """Test the service layer directly"""
    print("\n🔧 Testing Service Layer...")
    
    try:
        service = get_dolphin_service()
        response = await service.chat("Tell me a short joke")
        print(f"🤖 Direct service response: {response}")
    except Exception as e:
        print(f"❌ Direct service test failed: {e}")

def interactive_menu():
    """Interactive menu for different interaction methods"""
    print("🐬 Dolphin ByteDance Interactive Client")
    print("=" * 50)
    
    while True:
        print("\nChoose an interaction method:")
        print("1. 🌐 Test API endpoints")
        print("2. 💬 Test chat API")
        print("3. 🔧 Test direct service")
        print("4. 📖 Open API documentation")
        print("5. 🚀 Start server instructions")
        print("6. ❌ Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            asyncio.run(test_api_endpoints())
        elif choice == "2":
            asyncio.run(test_chat_api())
        elif choice == "3":
            asyncio.run(test_direct_service())
        elif choice == "4":
            print("📖 Open your browser to: http://127.0.0.1:8001/docs")
            print("   This shows interactive API documentation with a 'Try it out' feature")
        elif choice == "5":
            print("\n🚀 To start the Dolphin server:")
            print("cd backend")
            print("PYTHONPATH=$(pwd) python -m uvicorn dolphin_server:app --port 8001")
            print("\nThen visit: http://127.0.0.1:8001/docs for interactive API documentation")
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    # Check if API key is set
    api_key = os.getenv("DOLPHIN_API_KEY")
    if not api_key:
        print("⚠️  DOLPHIN_API_KEY not set - API calls will fail")
        print("   Set it with: export DOLPHIN_API_KEY='your-key'")
        print("   But you can still test the endpoints!\n")
    
    interactive_menu()