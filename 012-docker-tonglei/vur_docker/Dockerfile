FROM python:3.11-alpine AS base

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache gcc musl-dev libffi-dev g++ cmake make build-base

RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --disabled-password appuser && \
    chown -R appuser:appuser /app

FROM base AS final

COPY src .

USER appuser

ENV PORT=${PORT:-5000}
ENV LOG_LEVEL=${LOG_LEVEL:-info}

CMD ["python3", "main.py", "--port", "${PORT}", "--log-level", "${LOG_LEVEL}"]


