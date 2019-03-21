.PHONY: start-app start-server

docker: ## Start the docker environment
	@docker-compose up

start: ## Start the development server
	python manage.py runserver
