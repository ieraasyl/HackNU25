#!/bin/bash
# HackNU25 Backend Setup Script

echo "🚀 Setting up HackNU25 Backend Server..."

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found. Please run from HackNU25/backend directory."
    exit 1
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
../.venv/bin/pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env configuration file..."
    cp .env.example .env
    echo ""
    echo "📝 IMPORTANT: Edit .env file and add your GEMINI_API_KEY"
    echo "   Get your free API key from: https://makersuite.google.com/app/apikey"
    echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Get Gemini API key: https://makersuite.google.com/app/apikey"
echo "2. Edit .env file: nano .env"
echo "3. Add your API key: GEMINI_API_KEY=your_actual_key_here"  
echo "4. Run server: python main_server.py"
echo ""
echo "🌐 API docs will be at: http://127.0.0.1:8001/docs"