# 🦌 Local Dolphin Setup Guide - NO API KEYS NEEDED!

## 🚀 **Quick Start Options (Choose One)**

### **Option 1: Ollama (Recommended - Easiest!)**

Ollama makes running local AI models super simple on Mac:

#### Install Ollama:

```bash
# Download and install from website (easiest)
# Visit: https://ollama.ai and download for macOS

# OR install via command line:
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Pull and run Dolphin models:

```bash
# Start Ollama service
ollama serve

# In another terminal, pull a Dolphin model:
ollama pull dolphin-mistral        # ~4GB - Good balance
ollama pull dolphin-phi           # ~1.6GB - Smaller, faster
ollama pull codellama:7b          # ~3.8GB - Good for code

# Test it works:
ollama run dolphin-mistral "Hello! How are you?"
```

#### Your Dolphin service is now ready! 🎉

### **Option 2: Direct Transformers (More Control)**

If you want to load models directly in Python:

#### Install dependencies:

```bash
cd /Users/ualikhanyertayev/Desktop/dev/HackNU25/backend
/Users/ualikhanyertayev/Desktop/dev/HackNU25/.venv/bin/python -m pip install torch transformers accelerate
```

#### Download models:

```python
# This will download and cache models locally
from transformers import AutoTokenizer, AutoModelForCausalLM

# Download a smaller model first (to test)
model_name = "microsoft/DialoGPT-medium"  # ~350MB
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print("✅ Model downloaded and ready!")
```

### **Option 3: Mock Mode (Testing Only)**

For immediate testing without downloading anything, the service will run in mock mode and give demo responses.

---

## 🔧 **Configuration**

Your Dolphin service is already configured for local use! Check the settings:

```python
# In dolphin/config.py
provider = "local"          # ✅ Set to local
use_ollama = True          # ✅ Use Ollama (easiest)
ollama_model = "dolphin-mistral"  # ✅ Model to use
api_key = None             # ✅ No API key needed!
```

---

## 🧪 **Test Your Setup**

### Check if Ollama is working:

```bash
# Test Ollama directly
curl http://localhost:11434/api/tags

# Should return list of installed models
```

### Test through your API:

```bash
# Start your Dolphin server
cd /Users/ualikhanyertayev/Desktop/dev/HackNU25/backend
PYTHONPATH=/Users/ualikhanyertayev/Desktop/dev/HackNU25/backend /Users/ualikhanyertayev/Desktop/dev/HackNU25/.venv/bin/python -m uvicorn dolphin_server:app --port 8001

# Test the health endpoint
curl http://127.0.0.1:8001/api/v1/dolphin/health

# Test chat
curl -X POST "http://127.0.0.1:8001/api/v1/dolphin/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! How are you?"}'
```

---

## 💾 **Model Sizes & Performance**

| Model             | Size   | Speed  | Quality | Use Case        |
| ----------------- | ------ | ------ | ------- | --------------- |
| `dolphin-phi`     | ~1.6GB | Fast   | Good    | Quick responses |
| `dolphin-mistral` | ~4GB   | Medium | Great   | Balanced        |
| `codellama:7b`    | ~3.8GB | Medium | Great   | Code tasks      |
| `llama2:7b`       | ~3.8GB | Medium | Great   | General chat    |

**For your MacBook Pro with 24GB RAM**: Any of these will work great!

---

## 🔍 **Troubleshooting**

### "Cannot connect to Ollama"

```bash
# Make sure Ollama is running
ollama serve

# Check if it's listening
lsof -i :11434
```

### "Model not found"

```bash
# List installed models
ollama list

# Pull the model you want
ollama pull dolphin-mistral
```

### "Out of memory"

```bash
# Use a smaller model
ollama pull dolphin-phi

# Or adjust config for CPU-only
# In config.py: local_device = "cpu"
```

### Still not working?

The service will fall back to mock mode and still work for PDF processing and basic chat!

---

## 🎯 **Benefits of Local Setup**

✅ **Completely Free** - No API costs ever  
✅ **Private** - Your data never leaves your computer  
✅ **Offline** - Works without internet  
✅ **Fast** - No network latency  
✅ **Customizable** - You control everything

---

## 🚀 **Ready to Go!**

Once you've chosen and set up an option above, your Dolphin service will:

- ✅ Process PDFs locally
- ✅ Answer questions about documents
- ✅ Provide AI analysis
- ✅ Work completely offline
- ✅ Cost $0 to run

**No API keys, no cloud costs, no privacy concerns!** 🎉
