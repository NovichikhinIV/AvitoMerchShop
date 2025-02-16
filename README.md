# Тестовое задание для стажировки в Авито

## Запуск

перед запуском надо добавить .env файл в ./merch_service:
```
cd merch_service
cp .env.example .env
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
```
Далее добавляем pre-commit в Git-хуки. Теперь перед каждым git commit будут выполняться проверки:
```
pre-commit install
```
