# Dolphin ByteDance Integration

This module provides integration with ByteDance's Dolphin language model for chat functionality.

## Setup

### 1. Install Dependencies

The required dependencies should already be in the main `requirements.txt`:

- `httpx` - for HTTP requests
- `pydantic` - for configuration management
- `fastapi` - for API endpoints

### 2. Configure API Key

Set your ByteDance API key in the environment:

```bash
export DOLPHIN_API_KEY="your-api-key-here"
```

Or copy the example environment file:

```bash
cp dolphin/.env.example .env
# Edit .env and add your API key
```

### 3. Test the Integration

Run the test script to verify everything is working:

```bash
cd backend
python -m dolphin.test_dolphin
```

## Usage

### Basic Chat

```python
from dolphin.service import get_dolphin_service

# Simple chat
service = get_dolphin_service(api_key="your-key")
response = await service.chat("Hello, how are you?")
print(response)
```

### Streaming Chat

```python
# Streaming response
async for chunk in service.stream_chat("Tell me a story"):
    print(chunk, end="", flush=True)
```

### With Conversation History

```python
history = [
    {"role": "user", "content": "What's 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4."},
]

response = await service.chat(
    user_message="What about 3+3?",
    conversation_history=history
)
```

## API Endpoints

### REST Endpoints

- `POST /dolphin/chat` - Single chat message
- `POST /dolphin/chat/stream` - Streaming chat
- `GET /dolphin/health` - Health check

### WebSocket

- `WS /dolphin/ws` - Real-time chat WebSocket

Example WebSocket usage:

```javascript
const ws = new WebSocket("ws://localhost:8000/dolphin/ws");

ws.onopen = () => {
  ws.send(
    JSON.stringify({
      message: "Hello!",
      system_prompt: "You are a helpful assistant.",
    })
  );
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.response);
};
```

## Configuration

The integration can be configured via environment variables:

- `DOLPHIN_API_KEY` - Your ByteDance API key (required)
- `DOLPHIN_BASE_URL` - API base URL (default: ByteDance's endpoint)
- `DOLPHIN_MODEL_ENDPOINT` - Model endpoint ID
- `DOLPHIN_MAX_TOKENS` - Maximum tokens per response
- `DOLPHIN_TEMPERATURE` - Response randomness (0.0-1.0)
- `DOLPHIN_TIMEOUT` - Request timeout in seconds

## Files

- `client.py` - Low-level API client
- `service.py` - High-level service layer
- `config.py` - Configuration management
- `router.py` - FastAPI router with endpoints
- `test_dolphin.py` - Test script
- `.env.example` - Environment variables template

## Integration with Main App

To integrate with your main FastAPI app, add the router:

```python
from dolphin.router import router as dolphin_router

app.include_router(dolphin_router)
```

## Troubleshooting

1. **API Key Issues**: Make sure your ByteDance API key is valid and has access to the Dolphin model.

2. **Network Issues**: Check if you can reach the ByteDance API endpoint.

3. **Import Errors**: Make sure all dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

4. **Model Endpoint**: The default model endpoint is `ep-20241018143634-lwzsz`. You may need to update this based on your ByteDance account.

## Example Usage

See `test_dolphin.py` for complete working examples of all functionality.
