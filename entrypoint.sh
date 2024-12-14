#!/bin/bash
set -e

# Executar migrations ou outras tarefas
poetry run alembic upgrade head

# Executar o comando recebido
exec "$@"