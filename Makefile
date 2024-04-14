# Cleanup.
# =============================================================================

.PHONY: ruff clean

ruff:
	docker exec -ti htmx_django ruff check --fix htmx/ config/
	docker exec -ti htmx_django ruff format htmx/ config/

clean:
	find . -type d -name "__pycache__" -depth -exec rm -rf '{}' \;


# Django.
# =============================================================================

.PHONY: django_admin

# make django_admin
# make django_admin COMMAND=shell
# make django_admin COMMAND="loaddata fixtures/contact.json"
django_admin:
	docker exec -ti htmx_django django-admin $(COMMAND)


# Docker shell.
# =============================================================================

.PHONY: shell_on_django_container

shell_on_django_container:
	docker exec -ti htmx_django /bin/bash
