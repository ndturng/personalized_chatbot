# Define the default target
.DEFAULT_GOAL := help

# Build Docker containers
build:
	docker-compose build

# Run Docker containers and start nextjs app
run:
	docker-compose up -d
# create schema
create-schema:
	python data/weaviate_init.py schema
# upload sample data
upload-data:
	python data/weaviate_init.py upload
# check data
check-data:
	python data/weaviate_init.py check
# delete all data
delete-data:
	python data/weaviate_init.py delete
# query data
query-data:
	python data/query.py
# Stop Docker containers
stop:
	docker-compose down

# Display help message
help:
	@echo ""
	@echo "Available targets:"
	@echo "  help         Show this help message"
	@echo "  build        Build the Docker containers"
	@echo "  run          Run the Docker containers"
	@echo "  stop         Stop the Docker containers"
	@echo "  "
	@echo "  create-schema 				Create schema"
	@echo "  upload-data 				Upload sample data"
	@echo "  check-data 				Check data"
	@echo "  delete-data 				Delete all data"
