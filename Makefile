# Makefile for NovaHouse Chatbot
# Quick commands for common tasks

.PHONY: help install dev test lint format clean docker run deploy

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)NovaHouse Chatbot - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

dev: ## Setup development environment
	@echo "$(BLUE)Setting up development environment...$(NC)"
	python setup.py
	@echo "$(GREEN)✅ Development environment ready$(NC)"

test: ## Run tests with coverage
	@echo "$(BLUE)Running tests...$(NC)"
	pytest tests/ --cov=src --cov-report=term --cov-report=html
	@echo "$(GREEN)✅ Tests completed$(NC)"
	@echo "Coverage report: htmlcov/index.html"

test-fast: ## Run tests without coverage
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest tests/ -v
	@echo "$(GREEN)✅ Tests completed$(NC)"

lint: ## Run linters (flake8 + black check)
	@echo "$(BLUE)Running linters...$(NC)"
	flake8 src/ tests/
	black --check src/ tests/
	@echo "$(GREEN)✅ Linting completed$(NC)"

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	black src/ tests/
	isort src/ tests/
	@echo "$(GREEN)✅ Code formatted$(NC)"

clean: ## Clean cache and build files
	@echo "$(BLUE)Cleaning...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage coverage.xml
	@echo "$(GREEN)✅ Cleaned$(NC)"

docker: ## Build and run with Docker Compose
	@echo "$(BLUE)Starting Docker Compose...$(NC)"
	docker-compose up -d --build
	@echo "$(GREEN)✅ Docker containers running$(NC)"
	@echo "API: http://localhost:8080"

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Docker containers stopped$(NC)"

docker-logs: ## Show Docker logs
	docker-compose logs -f

run: ## Run development server locally
	@echo "$(BLUE)Starting development server...$(NC)"
	python main.py

smoke: ## Run smoke tests against production
	@echo "$(BLUE)Running smoke tests...$(NC)"
	python smoke_tests.py https://glass-core-467907-e9.ey.r.appspot.com
	@echo "$(GREEN)✅ Smoke tests completed$(NC)"

smoke-local: ## Run smoke tests against localhost
	@echo "$(BLUE)Running smoke tests (local)...$(NC)"
	python smoke_tests.py http://localhost:8080
	@echo "$(GREEN)✅ Smoke tests completed$(NC)"

deploy: ## Deploy to Google App Engine
	@echo "$(BLUE)Deploying to GCP...$(NC)"
	gcloud app deploy app.yaml --quiet
	@echo "$(GREEN)✅ Deployed to production$(NC)"

db-backup: ## Backup database
	@echo "$(BLUE)Creating database backup...$(NC)"
	curl -X POST http://localhost:8080/api/backup/manual -H "X-API-Key: ${API_KEY}"
	@echo "$(GREEN)✅ Backup created$(NC)"

pre-commit: ## Install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Pre-commit hooks installed$(NC)"

check: lint test ## Run all checks (lint + test)
	@echo "$(GREEN)✅ All checks passed$(NC)"

monitor: ## Monitor API performance in real-time
	@echo "$(BLUE)Starting performance monitor...$(NC)"
	./monitor.sh http://localhost:8080 5

monitor-prod: ## Monitor production API
	@echo "$(BLUE)Monitoring production...$(NC)"
	./monitor.sh https://glass-core-467907-e9.ey.r.appspot.com 10

check-deps: ## Check for outdated packages and available updates
	@echo "$(BLUE)Checking for updates...$(NC)"
	python check-deps.py

check-updates: check-deps ## Alias for check-deps (checks app + Python + packages)

update-deps: ## Update all Python packages to latest versions
	@echo "$(YELLOW)⚠️  Updating all packages...$(NC)"
	pip install --upgrade -r requirements.txt
	@echo "$(GREEN)✅ Packages updated. Run tests to verify!$(NC)"

vscode-extensions: ## Install recommended VSCode extensions
	@echo "$(BLUE)Installing VSCode extensions...$(NC)"
	./install-vscode-extensions.sh

setup-monitoring: ## Open monitoring setup guide
	@echo "$(BLUE)Opening monitoring setup guide...$(NC)"
	@cat SETUP_MONITORING.md

profile: ## Profile API performance (identify bottlenecks)
	@echo "$(BLUE)Profiling API performance...$(NC)"
	python profile_api.py --endpoint all --top 20

profile-chatbot: ## Profile chatbot endpoint only
	@echo "$(BLUE)Profiling chatbot endpoint...$(NC)"
	python profile_api.py --endpoint chatbot --top 15

load-test: ## Run load test with Locust (install: pip install locust)
	@echo "$(BLUE)Starting load test...$(NC)"
	@echo "$(YELLOW)📊 Open http://localhost:8089 to configure test$(NC)"
	locust -f locustfile.py --host=http://localhost:5000

load-test-prod: ## Run load test against production (⚠️ USE WITH CAUTION)
	@echo "$(RED)⚠️  WARNING: Testing production!$(NC)"
	@echo "$(YELLOW)📊 Open http://localhost:8089$(NC)"
	locust -f locustfile.py --host=https://glass-core-467907-e9.ey.r.appspot.com

load-test-smoke: ## Quick smoke test (10 users, 60s)
	@echo "$(BLUE)Running smoke test...$(NC)"
	locust -f locustfile.py --headless --users 10 --spawn-rate 2 --run-time 60s --host=http://localhost:5000

coverage-report: ## Generate and open coverage report
	@echo "$(BLUE)Generating coverage report...$(NC)"
	pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Opening coverage report...$(NC)"
	open htmlcov/index.html || xdg-open htmlcov/index.html 2>/dev/null

db-migrate: ## Create a new database migration
	@echo "$(BLUE)Creating new migration...$(NC)"
	alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

db-upgrade: ## Apply database migrations
	@echo "$(BLUE)Applying migrations...$(NC)"
	alembic upgrade head

db-downgrade: ## Rollback last migration
	@echo "$(YELLOW)Rolling back last migration...$(NC)"
	alembic downgrade -1

db-history: ## Show migration history
	@echo "$(BLUE)Migration history:$(NC)"
	alembic history

db-current: ## Show current migration version
	@echo "$(BLUE)Current version:$(NC)"
	alembic current

generate-clients: ## Generate API client SDKs (Python, TypeScript)
	@echo "$(BLUE)Generating API clients...$(NC)"
	./scripts/generate_clients.sh

generate-changelog: ## Generate CHANGELOG.md from git commits
	@echo "$(BLUE)Generating changelog...$(NC)"
	python scripts/generate_changelog.py
