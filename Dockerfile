# Этап 1: Сборка зависимостей и приложения
FROM python:3.13-alpine AS builder

# Установка переменных окружения
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # poetry
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.3

ENV PATH="$PATH:$POETRY_HOME/bin"

# Обновление пакетов и установка необходимых инструментов
RUN apk add --no-cache curl && \
    pip install --upgrade pip setuptools && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    apk del curl

WORKDIR /web

# Копируем зависимости проекта и устанавливаем их
COPY pyproject.toml poetry.lock ./

RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi && \
    rm -rf ~/.cache/pypoetry

# Этап 2: Финальный образ
FROM builder AS production

WORKDIR /web

# Копируем установленные зависимости из этапа сборки
COPY --from=builder /web /web

# Создаем нового пользователя
RUN adduser -D user

# Переключаемся на пользователя
USER user

# Копирование кода в контейнер
COPY --chown=user:user . .






