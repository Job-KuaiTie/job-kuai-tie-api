### Stage 1: Builder ###
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

# Install pipx & poetry
RUN pip install pipx && pipx ensurepath
RUN pipx install poetry && pipx inject poetry poetry-plugin-bundle

# Set workdir and copy project files
WORKDIR /app
COPY . .

# Explicitly specify the Python version to use in poetry bundle venv
RUN poetry bundle venv /venv --python /usr/local/bin/python3 --only=main

### Stage 2: Runtime ###
FROM gcr.io/distroless/python3-debian12

# Copy the venv and use its binary as entrypoint
COPY --from=builder /venv /venv

ENTRYPOINT ["/venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]