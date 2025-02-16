# Тестовое задание для стажировки в авито

## Запуск

перед запуском надо добавить .env файл в ./merch_service:
```
POSTGRES_DB=merch_db
POSTGRES_USER=merch_user
POSTGRES_PASSWORD=12345678
DB_HOST=merch_db
DB_PORT=5432

SECRET_KEY='o6p14wxvs8t=n4(oy9iywf$*4(jof%q9%t4q#pm6n6#hh)!t@8'
DEBUG=True
```

Затем запустить командой
```
docker-compose up --build
```

## Задание и решение

задание описано в файле task.md

backend: python, django rest framework

frontend: next.js

database: postgresql

## Конфигурация линтера

flake8:

.flake8
```
[flake8]
max-line-length = 80
exclude = .git,__pycache__,venv,__init__.py
ignore = E203, E266, E501, W503
```

black:

pyproject.toml
```
[tool.black]
line-length = 80
include = '\.pyi?$'
exclude = '''
/(
    migrations
    | venv
    | .git
    | __pycache__
)/
'''
```

isort:

.isort.cfg
```
[settings]
line_length = 80
include_trailing_comma = true
lines_after_imports = 2
skip = __init__.py

```

pre-commit:

.pre-commit-config.yaml
```
repos:
  - repo: local
    hooks:
      - id: isort
        name: isort
        entry: isort --settings-file ./.isort.cfg .
        language: system
        types: [python]
        pass_filenames: false

      - id: black
        name: black
        entry: black --config ./.black .
        language: system
        types: [python]
        pass_filenames: false

      - id: flake8
        name: flake8
        entry: flake8 --config ./.flake8 .
        language: system
        types: [python]
        pass_filenames: false
