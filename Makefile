# Define the default target
.DEFAULT_GOAL := help

# Build Docker containers
build:
	docker-compose build

# Run Docker containers and start nextjs app
run:
	docker-compose up -d
# create schema
weaviate-init-data:
	python scripts/weaviate_startup.py all

# delete all data
weaviate-delete-data:
	python scripts/weaviate_startup.py delete

# Stop Docker containers
stop:
	docker-compose down

# Display help message
help:
	@echo ""
	@echo "Available targets:"
	@echo "  build        Build the Docker containers"
	@echo "  run          Run the Docker containers"
	@echo "  stop         Stop the Docker containers"
	@echo "  weaviate-init-data          Create schema and import data"
	@echo "  weaviate-delete-data          Delete all data"
	@echo "  help         Show this help message"
