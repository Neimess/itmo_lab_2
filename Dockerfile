FROM texlive/texlive:latest
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /app

COPY . .

RUN uv sync --dev

CMD ["bash", "-c", "uv run pytest"]
