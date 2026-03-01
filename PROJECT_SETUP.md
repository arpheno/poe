# Path of Exile Tools - Project Setup Documentation

## Overview

This project is a comprehensive suite of tools for Path of Exile (POE), including:
- **Core POE library** (`poe/`): Business logic for trading, item valuation, filters, bulk trading, and ninja API integration
- **Django API backend** (`packages/your-api/`): REST API service
- **Angular frontend** (`packages/your-web/`): Web interface
- **Jupyter notebooks**: Analysis and experimentation tools for POE data

## Project Structure

```
poe/
├── poe/                      # Core POE tools library
│   ├── bulk/                 # Bulk trading functionality
│   ├── equipment_tracker/    # Equipment tracking
│   ├── filter/              # Loot filter tools
│   ├── fragment_sets/       # Fragment set management
│   ├── item/                # Item parsing and handling
│   ├── ninja/               # poe.ninja API integration
│   ├── proxy/               # Proxy handling
│   ├── sale/                # Sale tracking
│   ├── temple/              # Temple of Atzoatl tools
│   ├── trade/               # Trade API integration
│   ├── trade_finder/        # Trade finding algorithms
│   ├── valuation/           # Item valuation
│   └── woke/                # Awakened POE Trade integration
├── packages/
│   ├── your-api/            # Django REST API
│   ├── your-web/            # Angular frontend
│   ├── your-core/           # Shared core logic (if needed)
│   └── your-cli/            # CLI tools (if needed)
├── notebooks/               # Jupyter notebooks for analysis
│   ├── awakened.ipynb
│   ├── lootfilter.ipynb
│   ├── stash tabs.ipynb
│   ├── tab_analyzer.ipynb
│   └── ... (various analysis notebooks)
├── reports/                 # Generated analysis reports
├── docker/                  # Docker configurations
├── Makefile                 # Development commands
├── pyproject.toml          # Root project configuration
├── requirements.txt        # Compiled Python dependencies
└── docker-compose.yml      # Docker orchestration
```

## Prerequisites

- **Python**: 3.11 (required, <3.12)
- **uv**: Fast Python package manager (`pip install uv`)
- **Node.js**: 18+ (for frontend)
- **Docker & Docker Compose**: For containerized deployment
- **Make**: For using Makefile commands (optional but recommended)

## Quick Start (Recommended)

### 1. Clone and Enter the Project
```bash
git clone <repository-url>
cd poe
```

### 2. Install Python Dependencies
Using `uv` (recommended):
```bash
make install
```

Or install for development (includes test/lint tools):
```bash
make install-dev
```

Manual installation:
```bash
uv pip install -e .
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root (copy from `.env` if it exists).

Required environment variables:
```bash
# Django settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Backend URL for frontend
BACKEND_URL=http://localhost:8000
```

### 4. Run Database Migrations
```bash
make migrate
```

### 5. Run the Application

**Option A: Development Mode (separate services)**

Terminal 1 - API:
```bash
make run-api
```

Terminal 2 - Frontend:
```bash
make run-web
```

**Option B: Docker (full stack)**
```bash
make docker-build
make docker-up
```

### 6. Access the Application
- **API**: http://localhost:8000
- **Web Interface**: http://localhost:4200

## Makefile Commands Reference

The project uses a Makefile for common development tasks. All commands should be run from the project root.

### Installation
```bash
make install          # Install production dependencies
make install-dev      # Install dev dependencies (includes pytest, flake8, mypy, black, isort)
```

### Testing & Quality
```bash
make test            # Run tests with coverage on packages/ and poe/
make lint            # Run linting (flake8, mypy, black --check, isort --check)
make format          # Format code (black, isort)
```

### Django Management
```bash
make migrate         # Run Django migrations
make makemigrations  # Create new Django migrations
make collectstatic   # Collect static files
```

### Development Servers
```bash
make run-api         # Start Django development server (port 8000)
make run-web         # Start Angular development server (port 4200)
```

### Docker
```bash
make docker-build    # Build Docker containers
make docker-up       # Start all services with docker-compose
make docker-down     # Stop all services
```

### Cleanup
```bash
make clean          # Remove build artifacts, cache files, coverage reports
```

### Default Target
```bash
make                # Runs 'make install' and 'make test'
```

## Development Workflows

### Working on Core POE Library

1. Make changes to files in `poe/`
2. Format code:
   ```bash
   make format
   ```
3. Run tests:
   ```bash
   make test
   ```
4. Check for issues:
   ```bash
   make lint
   ```

### Working with Jupyter Notebooks

Start Jupyter Lab:
```bash
jupyter lab
```

Available notebooks:
- `awakened.ipynb` - Awakened POE Trade integration
- `lootfilter.ipynb` - Loot filter analysis
- `stash tabs.ipynb` - Stash tab management
- `tab_analyzer.ipynb` - Tab analysis tools
- `value.ipynb` - Item valuation
- And more experimental notebooks

### Working on Django API

1. Navigate to API directory:
   ```bash
   cd packages/your-api
   ```

2. Create migrations after model changes:
   ```bash
   make makemigrations
   ```

3. Apply migrations:
   ```bash
   make migrate
   ```

4. Run development server:
   ```bash
   make run-api
   ```

### Working on Frontend

1. Navigate to web directory:
   ```bash
   cd packages/your-web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm start
   # or from project root: make run-web
   ```

## Docker Deployment

### Build and Run
```bash
# Build containers
make docker-build

# Start all services
make docker-up

# View logs
docker-compose logs -f

# Stop services
make docker-down
```

### Services in Docker Compose
- **backend**: Django API service
  - Port: 8000
  - Volumes: `poe/`, `packages/your-api/`
  - Auto-runs migrations and collectstatic on startup
  
- **frontend**: Angular web application
  - Port: 4200 (mapped to 80 in container)
  - Depends on backend service

## Dependencies

### Core POE Library Dependencies
- **pandas**: Data manipulation and analysis
- **requests**: HTTP library for API calls
- **aiohttp**: Async HTTP client
- **websockets**: WebSocket support for real-time data
- **lxml**: XML/HTML parsing
- **pydantic**: Data validation
- **scipy**: Scientific computing
- **pendulum**: DateTime library
- **gitpython**: Git integration
- **redislite**: Redis database (embedded)
- **dataenforce**: Data validation

### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **flake8**: Linting
- **mypy**: Static type checking
- **black**: Code formatting
- **isort**: Import sorting

### Jupyter & Analysis
- **jupyter**: Notebook environment
- **matplotlib**: Plotting
- **seaborn**: Statistical visualization
- **plotly**: Interactive plots
- **jupyterthemes**: Notebook themes

### Web Stack
- **django**: Web framework
- **django-cors-headers**: CORS handling
- **Angular**: Frontend framework (in packages/your-web/)

## Configuration Files

- **pyproject.toml**: Root Python project config (Poetry-based)
- **poe/pyproject.toml**: POE library package config
- **requirements.txt**: Compiled dependencies (auto-generated by uv)
- **docker-requirements.txt**: Docker-specific dependencies
- **Makefile**: Development command shortcuts
- **docker-compose.yml**: Docker orchestration
- **.env**: Environment variables (create this file)

## Testing

Run the full test suite:
```bash
make test
```

This runs pytest with coverage on:
- `packages/` - All package code
- `poe/` - Core POE library

Coverage reports are generated in:
- `.coverage` - Coverage data
- `htmlcov/` - HTML coverage report (view with browser)

## Code Quality

### Format Code
```bash
make format
```
Runs:
- `black` - Code formatter
- `isort` - Import sorter

### Check Code Quality
```bash
make lint
```
Runs:
- `flake8` - Style guide enforcement
- `mypy` - Static type checking
- `black --check` - Format verification
- `isort --check` - Import order verification

## Troubleshooting

### Python Version Issues
This project requires Python 3.11 (specifically >=3.11, <3.12). Check your version:
```bash
python --version
```

### Missing Dependencies
If you get import errors:
```bash
make install-dev  # Installs all dependencies
```

### Database Issues
Reset database:
```bash
cd packages/your-api
rm db.sqlite3  # If using SQLite
make migrate
```

### Docker Issues
Clean rebuild:
```bash
make docker-down
docker-compose down -v  # Remove volumes
make docker-build
make docker-up
```

### Port Already in Use
If port 8000 or 4200 is in use:
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
lsof -ti:4200 | xargs kill -9
```

## Common Tasks

### Adding a New Python Dependency
1. Edit `pyproject.toml` (add to `[tool.poetry.dependencies]`)
2. Regenerate requirements:
   ```bash
   uv pip compile pyproject.toml -o requirements.txt
   ```
3. Install:
   ```bash
   make install
   ```

### Running Specific Tests
```bash
pytest tests/test_specific.py
pytest tests/test_specific.py::test_function
```

### Viewing Coverage Report
```bash
make test
open htmlcov/index.html  # macOS
```

### Cleaning Build Artifacts
```bash
make clean
```

## Project Background

This is a toolkit for Path of Exile that includes:
- **Trading tools**: Automated trading, bulk trading, trade finding
- **Item analysis**: Valuation, filtering, equipment tracking
- **API integrations**: POE Trade API, poe.ninja
- **Data analysis**: Jupyter notebooks for market analysis
- **Web interface**: Django + Angular full-stack application

## Additional Resources

- Path of Exile Trade API: https://www.pathofexile.com/trade
- poe.ninja: https://poe.ninja
- Django Documentation: https://docs.djangoproject.com/
- Angular Documentation: https://angular.io/docs

## Getting Help

- Check the Makefile for available commands: `cat Makefile`
- Review test files in `tests/` for usage examples
- Examine Jupyter notebooks for analysis workflows
- Check Docker logs: `docker-compose logs -f`
