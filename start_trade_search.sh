#!/bin/bash

# Startup script for PoE Trade Search

echo "🔥 Starting PoE Trade Search System..."
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install Python dependencies if needed
echo "📦 Checking Python dependencies..."
pip install -q flask flask-cors requests

# Start the proxy in background
echo "🌐 Starting proxy server on port 8999..."
python poe/proxy/main.py > proxy.log 2>&1 &
PROXY_PID=$!
echo "   Proxy PID: $PROXY_PID"

# Wait a moment for proxy to start
sleep 2

# Start the Flask API in background
echo "🚀 Starting Flask API on port 5000..."
python poe/api/search_api.py > api.log 2>&1 &
API_PID=$!
echo "   API PID: $API_PID"

# Wait a moment for API to start
sleep 2

# Start the Vue frontend
echo "⚡ Starting Vue frontend on port 3000..."
cd frontend/poe-trade-search

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

echo ""
echo "✅ All services started!"
echo ""
echo "📊 Access the application at: http://localhost:3000"
echo "🔧 API available at: http://localhost:5000"
echo "🌐 Proxy running at: http://localhost:8999"
echo ""
echo "📝 Logs:"
echo "   - Proxy: proxy.log"
echo "   - API: api.log"
echo ""
echo "To stop all services:"
echo "   kill $PROXY_PID $API_PID"
echo "   Or press Ctrl+C and run: pkill -f 'python.*proxy' && pkill -f 'python.*search_api'"
echo ""

# Start Vue dev server (this will block)
npm run dev

# Cleanup when Vue dev server exits
echo ""
echo "🛑 Shutting down services..."
kill $PROXY_PID $API_PID 2>/dev/null
echo "✅ Services stopped"
