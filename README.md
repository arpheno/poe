# Your Project Name

A comprehensive platform for [brief description of your project].

## Project Structure

```
your-project/
├── packages/
│   ├── your-core/       # Core business logic (if needed)
│   ├── your-cli/        # Command-line interface (if needed)
│   ├── your-api/        # Django REST API service
│   └── your-web/        # Angular frontend
├── poe/                 # Core business logic for Path of Exile tools
├── docker/              # Docker-related configurations
├── .github/             # GitHub Actions and configuration
├── docker-compose.yml   # Docker Compose configuration
├── backend.Dockerfile   # Backend Dockerfile
├── pyproject.toml       # Python project configuration
├── Makefile             # Development workflow commands
└── README.md            # Project documentation
```

## Prerequisites

* Python 3.11 or higher
* Node.js 18 or higher
* Docker and Docker Compose
* Make (optional, for using Makefile commands)
* uv (for Python dependency management)

## Development Setup

### Quick Start

```bash
# Clone the repository
git clone [your-repository-url]
cd [your-project-directory]

# Install uv if not already installed
pip install uv

# Setup backend
uv pip install -e .

# Setup frontend
cd packages/your-web
npm install
cd ../..

# Run the application with Docker
docker-compose up --build
```

### Detailed Setup

#### Backend (API and Core)

1. Install dependencies with uv:
   ```bash
   uv pip install -e .
   ```

2. Run migrations:
   ```bash
   make migrate
   ```

3. Run the Django development server:
   ```bash
   make run-api
   ```

#### Frontend

1. Install dependencies:
   ```bash
   cd packages/your-web
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```
   or
   ```bash
   make run-web
   ```

## Docker Setup

To run the entire stack using Docker:

```bash
docker-compose up --build
```

Services:
* API: http://localhost:8000
* Web Interface: http://localhost:4200

## Testing

Run tests with:

```bash
make test
```

## Linting and Formatting

```bash
# Run linters
make lint

# Format code
make format
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Create a pull request

## License

[Your License] 