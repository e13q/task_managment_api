update: ## Обновляет local-окружение: скачивает и пересобирает докер-образы, применяет миграции и создаёт суперпользователя
	docker compose pull --ignore-buildable
	docker compose build
	make migrate
	docker compose run --rm django bash -c '\
		until curl -s http://elasticsearch:9200 > /dev/null; do \
			echo "Waiting for Elasticsearch..."; \
			sleep 3; \
		done \
	'
	docker compose run --rm django ./manage.py createsuperuser --no-input; true
	docker compose run --rm django ./manage.py search_index --rebuild -f
	@echo "Update done successfully."

makemigrations: ## Создаёт новые файлы миграций Django ORM
	docker compose run --rm django ./manage.py makemigrations

migrate: ## Применяет новые миграции Django ORM
	docker compose run --rm django ./manage.py migrate