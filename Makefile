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

setup-monitoring: ## Open monitoring setup guide
	@echo "$(BLUE)Opening monitoring setup guide...$(NC)"
	@cat SETUP_MONITORING.md
