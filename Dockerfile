FROM python:3.12-slim

# Configurações do Python e do uv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Instala o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copia os arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instala as dependências
RUN uv sync --frozen --no-dev --no-install-project

# Copia o código e os dados JSON
COPY . .

# Inicia a API
CMD ["uvicorn", "gerador_nfce:app", "--host", "0.0.0.0", "--port", "8080"]