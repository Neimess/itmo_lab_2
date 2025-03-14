FROM debian:bookworm-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


RUN apt-get update && apt-get install -y \
    texlive-xetex texlive-latex-base \
    && rm -rf /var/lib/apt/lists/

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID user && useradd -m -u $UID -g $GID user

WORKDIR /app
RUN chown -R user:user /app


USER user

COPY --chown=user:user . .

RUN uv sync --dev

CMD ["bash", "-c", "uv run src/main.py"]
