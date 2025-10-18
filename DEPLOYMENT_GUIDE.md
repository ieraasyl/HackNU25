# Dolphin AI Setup for Organization Team

## 🎯 Quick Start Options

### Option 1: Local Development (Each Developer)

```bash
# 1. Clone repository
git clone https://github.com/your-org/HackNU25
cd HackNU25/backend

# 2. Install Ollama
brew install ollama  # macOS
# OR: curl -fsSL https://ollama.ai/install.sh | sh  # Linux

# 3. Start Ollama & Download model
brew services start ollama
ollama pull dolphin-mistral

# 4. Run Dolphin server
./setup_local_dolphin.sh
```

### Option 2: Cloud API (Production)

```bash
# Set environment variables
export PROVIDER=bytedance
export BYTEDANCE_API_KEY=your_team_api_key

# Run server
uvicorn dolphin_server:app --host 0.0.0.0 --port 8001
```

### Option 3: Docker Deployment

```bash
# Build and run
docker-compose up -d
```

## 🔧 Configuration Options

| Mode            | Setup Required              | Cost                | AI Quality | Scalability    |
| --------------- | --------------------------- | ------------------- | ---------- | -------------- |
| Local Ollama    | Install on each dev machine | Free                | High       | Single machine |
| ByteDance Cloud | API key only                | Pay per use         | Very High  | Unlimited      |
| Docker + Cloud  | Container deployment        | Infrastructure cost | High       | High           |

## 📋 Current Status

- ✅ Local Ollama: Working (your machine)
- 🔧 ByteDance API: Needs API key setup
- 🔧 Docker: Ready for deployment
- ✅ Mock Mode: Always works (fallback)

## 🚀 Recommended for Organization

**Development**: Local Ollama (each developer installs)
**Production**: ByteDance Doubao API (shared team credentials)
**Fallback**: Mock mode (always available)

## 🔑 Team API Key Setup

Contact ByteDance for organization API key:

- Website: https://www.volcengine.com/products/doubao
- Apply for team/organization account
- Set environment variable: `BYTEDANCE_API_KEY=your_key`

## 🧪 Testing

```bash
# Test current setup
curl -X POST "http://localhost:8001/api/v1/dolphin/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI!"}'

# Test PDF processing
curl -X POST "http://localhost:8001/api/v1/dolphin/ask-pdf" \
  -F "file=@test.pdf" \
  -F "question=What is this document about?"
```
