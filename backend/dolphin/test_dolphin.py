import asyncio
import os
from dolphin.service import get_dolphin_service
from dolphin.client import chat_with_dolphin

async def test_dolphin_basic():
    """Test basic Dolphin ByteDance functionality"""
    
    # Check if API key is available
    api_key = os.getenv("DOLPHIN_API_KEY")
    if not api_key:
        print("❌ DOLPHIN_API_KEY environment variable not set")
        print("Please set your ByteDance API key:")
        print("export DOLPHIN_API_KEY='your-api-key-here'")
        return False
    
    print("🐬 Testing Dolphin ByteDance integration...")
    
    try:
        # Test simple chat function
        print("\n1. Testing simple chat function...")
        response = await chat_with_dolphin(
            message="Hello! Please respond with 'Dolphin is working correctly'",
            api_key=api_key
        )
        print(f"✅ Simple chat response: {response[:100]}...")
        
        # Test service layer
        print("\n2. Testing service layer...")
        service = get_dolphin_service(api_key=api_key)
        
        response = await service.chat(
            user_message="What is 2+2?",
            system_prompt="You are a helpful math assistant."
        )
        print(f"✅ Service response: {response[:100]}...")
        
        # Test streaming (just check if it starts)
        print("\n3. Testing streaming response...")
        stream_started = False
        async for chunk in service.stream_chat(
            user_message="Count to 3",
            system_prompt="Count numbers one by one."
        ):
            if not stream_started:
                print(f"✅ Streaming started: {chunk}")
                stream_started = True
                break
        
        print("\n🎉 All tests passed! Dolphin ByteDance is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Dolphin: {e}")
        print("\nPossible issues:")
        print("- Check your API key")
        print("- Verify network connectivity")
        print("- Ensure ByteDance API is accessible")
        return False

async def test_dolphin_config():
    """Test Dolphin configuration"""
    print("\n🔧 Testing Dolphin configuration...")
    
    try:
        from dolphin.config import dolphin_config
        
        print(f"Base URL: {dolphin_config.base_url}")
        print(f"Model Endpoint: {dolphin_config.model_endpoint}")
        print(f"Max Tokens: {dolphin_config.max_tokens}")
        print(f"Temperature: {dolphin_config.temperature}")
        print(f"Timeout: {dolphin_config.timeout}")
        
        api_key_set = "✅" if dolphin_config.api_key else "❌"
        print(f"API Key: {api_key_set} {'Set' if dolphin_config.api_key else 'Not set'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting Dolphin ByteDance tests...\n")
    
    config_ok = await test_dolphin_config()
    basic_ok = await test_dolphin_basic()
    
    print(f"\n📊 Test Results:")
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Basic functionality: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    
    if config_ok and basic_ok:
        print("\n🎉 Dolphin ByteDance is ready to use!")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")

if __name__ == "__main__":
    asyncio.run(main())