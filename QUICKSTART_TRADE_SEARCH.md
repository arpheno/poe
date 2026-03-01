# PoE Trade Search - Quick Start

## Setup (One Time)

```bash
make install-trade-search
```

This installs:
- Flask and flask-cors for the API
- npm dependencies for the Vue frontend

## Running the Application

### Option 1: Full Dev Environment (Recommended)

```bash
make trade-dev
```

This starts:
1. Proxy server (port 8999) - in background
2. Flask API (port 5000) - in background  
3. Vue dev server (port 3000) - in foreground

Access the app at: **http://localhost:3000**

### Option 2: Start Services Individually

```bash
# Terminal 1: Start proxy
make start-proxy

# Terminal 2: Start API
make start-trade-api

# Terminal 3: Start frontend
make start-trade-frontend
```

## Stopping Services

```bash
make trade-stop
```

Stops all background services (proxy and API). The frontend will stop when you Ctrl+C it.

## Checking Status

```bash
make trade-check
```

Shows which services are running:
- ✅ = Running
- ❌ = Not running

## Viewing Logs

```bash
make trade-logs
```

Tails the logs for proxy and API. Press Ctrl+C to exit.

## Troubleshooting

### Services won't start

```bash
# Stop everything first
make trade-stop

# Check what's running
make trade-check

# Clean up
make clean

# Try again
make trade-dev
```

### Port already in use

If you get "address already in use" errors:

```bash
# Find what's using the port
lsof -i :8999  # proxy
lsof -i :5000  # API
lsof -i :3000  # frontend

# Kill the process
kill -9 <PID>
```

### Frontend not connecting to API

1. Check API is running: `curl http://localhost:5000/api/health`
2. Check proxy is running: `curl http://localhost:8999/api/trade/data/static`
3. Look at logs: `make trade-logs`

## Full Command Reference

```bash
# Setup
make install-trade-search    # Install all dependencies

# Running
make trade-dev               # Start everything (proxy + API + frontend)
make start-proxy             # Start proxy only (background)
make start-trade-api         # Start API only (background)
make start-trade-frontend    # Start frontend only (foreground)

# Management
make trade-stop              # Stop all services
make trade-restart           # Restart all services
make trade-check             # Health check
make trade-logs              # View logs

# Cleanup
make clean                   # Clean logs and build artifacts
```

## How It Works

```
┌─────────────────┐
│   Vue Frontend  │  (Port 3000)
│  User Interface │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   Flask API     │  (Port 5000)
│  Query Builder  │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   Proxy Server  │  (Port 8999)
│  Rate Limiting  │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│  PoE Trade API  │  (pathofexile.com)
└─────────────────┘
```

## Files Created

```
poe/
├── Makefile                               # Build commands
├── poe/api/search_api.py                 # Flask API
├── frontend/poe-trade-search/            # Vue app
│   ├── src/App.vue                       # Main component
│   ├── package.json                      # npm deps
│   └── vite.config.js                    # Vite config
└── logs/                                 # Runtime logs
    ├── proxy.log
    ├── trade-api.log
    ├── proxy.pid
    └── trade-api.pid
```

## Next Steps

1. `make install-trade-search` - Install dependencies
2. `make trade-dev` - Start the app
3. Open http://localhost:3000
4. Start searching!
