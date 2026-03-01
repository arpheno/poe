.PHONY: install install-dev test lint format clean docker-build docker-up docker-down \
        install-trade-search start-proxy start-trade-api start-trade-frontend trade-dev trade-stop trade-logs trade-check

# Default target
all: install test

# Install production dependencies
install:
	uv pip install .

# Install development dependencies
install-dev:
	uv pip install -e .
	uv pip install pytest pytest-cov flake8 mypy black isort

# Run tests with coverage
test:
	uv run pytest --cov=packages --cov=poe

# Run linting
lint:
	uv run flake8 packages poe
	uv run mypy packages poe
	uv run black --check packages poe
	uv run isort --check packages poe

# Format code
format:
	uv run black packages poe
	uv run isort packages poe

# Clean up build artifacts
clean:
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

# Django commands
migrate:
	cd packages/your-api && uv run python manage.py migrate

makemigrations:
	cd packages/your-api && uv run python manage.py makemigrations

collectstatic:
	cd packages/your-api && uv run python manage.py collectstatic --no-input

# Run development servers
run-api:
	cd packages/your-api && uv run python manage.py runserver

run-web:
	cd packages/your-web && npm start

# ============================================================================
# Trade Search Application
# ============================================================================

# Install trade search dependencies
install-trade-search:
	@echo "📦 Installing trade search dependencies..."
	uv pip install flask flask-cors
	cd frontend/poe-trade-search && npm install
	@echo "✅ Trade search dependencies installed"

# Start the PoE API proxy
start-proxy:
	@echo "🌐 Starting proxy server on port 8999..."
	@mkdir -p logs
	@nohup uv run python poe/proxy/main.py > logs/proxy.log 2>&1 & echo $$! > logs/proxy.pid
	@echo "   Proxy PID: $$(cat logs/proxy.pid)"
	@echo "   Logs: logs/proxy.log"

# Start the Flask API
start-trade-api:
	@echo "🚀 Starting Flask API on port 5000..."
	@mkdir -p logs
	@nohup uv run python poe/api/search_api.py > logs/trade-api.log 2>&1 & echo $$! > logs/trade-api.pid
	@echo "   API PID: $$(cat logs/trade-api.pid)"
	@echo "   Logs: logs/trade-api.log"

# Start the Vue frontend dev server
start-trade-frontend:
	@echo "⚡ Starting Vue frontend on port 3000..."
	@cd frontend/poe-trade-search && npm run dev

# Start full trade search dev environment
trade-dev: start-proxy
	@echo "⏳ Waiting for proxy to initialize..."
	@sleep 2
	@$(MAKE) start-trade-api
	@sleep 1
	@echo ""
	@echo "✅ Backend services started!"
	@echo "🌐 Proxy: http://localhost:8999 (PID: $$(cat logs/proxy.pid))"
	@echo "🚀 API: http://localhost:5000 (PID: $$(cat logs/trade-api.pid))"
	@echo "📊 Frontend: http://localhost:3000"
	@echo ""
	@echo "🔍 Starting frontend..."
	@$(MAKE) start-trade-frontend

# Stop all trade search services
trade-stop:
	@echo "🛑 Stopping trade search services..."
	@if [ -f logs/trade-api.pid ]; then \
		kill $$(cat logs/trade-api.pid) 2>/dev/null && echo "   ✓ Stopped API" || echo "   ⚠ API already stopped"; \
		rm -f logs/trade-api.pid; \
	fi
	@if [ -f logs/proxy.pid ]; then \
		kill $$(cat logs/proxy.pid) 2>/dev/null && echo "   ✓ Stopped Proxy" || echo "   ⚠ Proxy already stopped"; \
		rm -f logs/proxy.pid; \
	fi
	@pkill -f "vite.*poe-trade-search" 2>/dev/null && echo "   ✓ Stopped Vite" || true
	@echo "✅ All trade search services stopped"

# View trade search logs
trade-logs:
	@echo "📝 Tailing trade search logs (Ctrl+C to exit)..."
	@tail -f logs/proxy.log logs/trade-api.log 2>/dev/null || echo "❌ No logs found. Run 'make trade-dev' first."

# Check trade search service health
trade-check:
	@echo "🔍 Checking trade search services..."
	@echo -n "Proxy (8999): "
	@curl -s http://localhost:8999/api/trade/data/static >/dev/null 2>&1 && echo "✅" || echo "❌"
	@echo -n "API (5000): "
	@curl -s http://localhost:5000/api/health >/dev/null 2>&1 && echo "✅" || echo "❌"
	@echo -n "Frontend (3000): "
	@curl -s http://localhost:3000 >/dev/null 2>&1 && echo "✅" || echo "❌"

# Restart trade search services
trade-restart: trade-stop trade-dev
	@echo "♻️  Trade search services restarted"

# Run the full stack (Proxy, Backend, Frontend)
run:
	docker-compose up --build