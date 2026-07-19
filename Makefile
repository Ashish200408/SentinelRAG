.PHONY: backend frontend docker lint format test run

backend:
	cd backend && uv run uvicorn app.main:app --reload

frontend:
	cd frontend && pnpm run dev

docker:
	docker-compose -f docker/compose/docker-compose.dev.yml up --build

lint:
	cd backend && uv run ruff check .
	cd frontend && pnpm run lint

format:
	cd backend && uv run ruff format .
	cd frontend && pnpm run format

test:
	cd backend && uv run pytest
	cd frontend && pnpm run test

run: docker
