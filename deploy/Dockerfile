FROM python:3.12-slim@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/opt/forge UV_PYTHON_DOWNLOADS=never
COPY pyproject.toml uv.lock /app/
RUN pip install --no-cache-dir uv==0.13.9 && uv sync --locked --extra service --extra schemas --no-dev
RUN useradd --uid 10001 --create-home agent && mkdir /data && chown agent:agent /data
COPY forgeagent /app/forgeagent
COPY deploy/asgi.py /app/deploy/asgi.py
USER agent
ENV FORGEAGENT_DATABASE=/data/jobs.sqlite3
EXPOSE 8000
CMD ["/opt/forge/bin/uvicorn", "deploy.asgi:create_application", "--factory", "--host", "0.0.0.0", "--port", "8000"]
