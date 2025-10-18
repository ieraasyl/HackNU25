#!/bin/bash

# 🦌 Dolphin Local Setup Script
# This script installs Ollama and sets up Dolphin models locally

echo "🦌 Setting up Local Dolphin - NO API KEYS NEEDED!"
echo "================================================"

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This script is designed for macOS. For other systems, visit https://ollama.ai"
    exit 1
fi

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed!"
    ollama --version
else
    echo "📦 Installing Ollama..."
    
    # Check if we can use curl
    if command -v curl &> /dev/null; then
        curl -fsSL https://ollama.ai/install.sh | sh
        
        if [ $? -eq 0 ]; then
            echo "✅ Ollama installed successfully!"
        else
            echo "❌ Ollama installation failed. Please visit https://ollama.ai to install manually."
            exit 1
        fi
    else
        echo "❌ curl not found. Please visit https://ollama.ai to install Ollama manually."
        exit 1
    fi
fi

echo ""
echo "🚀 Starting Ollama service..."

# Start Ollama in background if not running
if ! pgrep -f "ollama serve" > /dev/null; then
    ollama serve &
    sleep 3
    echo "✅ Ollama service started"
else
    echo "✅ Ollama service already running"
fi

echo ""
echo "📥 Available Dolphin models:"
echo "1. dolphin-mistral (4GB) - Recommended balance of speed/quality"
echo "2. dolphin-phi (1.6GB) - Smaller, faster"
echo "3. codellama:7b (3.8GB) - Great for code analysis"

echo ""
read -p "Which model would you like to install? (1/2/3) [1]: " choice
choice=${choice:-1}

case $choice in
    1)
        MODEL="dolphin-mistral"
        SIZE="~4GB"
        ;;
    2)
        MODEL="dolphin-phi"
        SIZE="~1.6GB"
        ;;
    3)
        MODEL="codellama:7b"
        SIZE="~3.8GB"
        ;;
    *)
        MODEL="dolphin-mistral"
        SIZE="~4GB"
        echo "Invalid choice, defaulting to dolphin-mistral"
        ;;
esac

echo ""
echo "📥 Downloading $MODEL ($SIZE)..."
echo "⏳ This may take a few minutes depending on your internet connection..."

ollama pull $MODEL

if [ $? -eq 0 ]; then
    echo "✅ Model $MODEL downloaded successfully!"
else
    echo "❌ Failed to download $MODEL. Check your internet connection and try again."
    exit 1
fi

echo ""
echo "🧪 Testing the model..."
response=$(ollama run $MODEL "Hello! Please respond with just 'OK' to confirm you're working." --format json 2>/dev/null | tail -n 1)

if [[ $response == *"OK"* ]] || [[ $response == *"ok"* ]]; then
    echo "✅ Model test successful!"
else
    echo "⚠️  Model test inconclusive, but model should be ready to use."
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "✅ Ollama installed and running"
echo "✅ Model '$MODEL' ready to use"
echo "✅ Your Dolphin service will now work locally!"
echo ""
echo "🚀 Next steps:"
echo "1. Start your Dolphin server:"
echo "   cd backend && python dolphin_server.py"
echo ""
echo "2. Visit http://localhost:8001/docs to test it!"
echo ""
echo "3. Upload PDFs and chat - everything runs locally! 🔒"
echo ""
echo "💡 To use a different model later:"
echo "   ollama pull <model-name>"
echo "   Then update dolphin/config.py with the new model name."
echo ""
echo "🔍 Troubleshooting:"
echo "   • List models: ollama list"
echo "   • Check service: ollama serve"
echo "   • Test model: ollama run $MODEL 'Hello'"