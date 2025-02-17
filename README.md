# Тестовое задание для стажировки в Авито

## Запуск

перед запуском надо добавить .env файл в ./merch_service:
```
cd merch_service
cp .env.example .env
cd ..
```

Затем запустить командой
```
docker-compose up --build -d
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
exclude = .git,__pycache__,venv,__init__.py,node_modules
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
profile = black
line_length = 80
include_trailing_comma = true
lines_after_imports = 2
skip = __init__.py,.git,__pycache__,venv,node_modules
```

pre-commit:

.pre-commit-config.yaml
```
repos:
  - repo: local
    hooks:
      - id: isort
        name: isort
        entry: isort --settings-file ./merch_service/.isort.cfg .
        language: system
        types: [python]
        pass_filenames: false
        files: "^merch_service/.*\\.py$"

      - id: black
        name: black
        entry: black --config ./merch_service/pyproject.toml .
        language: system
        types: [python]
        pass_filenames: false
        files: "^merch_service/.*\\.py$"

      - id: flake8
        name: flake8
        entry: flake8 --config ./merch_service/.flake8 .
        language: system
        types: [python]
        pass_filenames: false
        files: "^merch_service/.*\\.py$"
```
Далее добавляем pre-commit в Git-хуки. Теперь перед каждым git commit будут выполняться проверки:
```
pre-commit install
```
