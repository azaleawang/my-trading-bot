.PHONY: env-example

env-example:
	@if [ ! -f .env ]; then \
		echo ".env file not found"; \
		exit 1; \
	fi
	@if [ ! -f .env.example ]; then \
		touch .env.example; \
	fi
	@cat .env | grep -v '^#' | grep -v '^$$' | sed 's/=.*//' | while read -r key; do \
		if ! grep -q "^$$key=" .env.example; then \
			echo "$$key=" >> .env.example; \
		fi \
	done
	@echo "Updated .env.example with new keys from .env"
