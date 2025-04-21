# Use official Python image
FROM python:3.13-slim

# Set environment variables
# No need .pyc file
ENV PYTHONDONTWRITEBYTECODE 1
# No delay in logs
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtualenv
RUN poetry config virtualenvs.create false \
# --no-interaction: Prevents Poetry from prompting user input
# --no-ansi: Disables colored output and fancy formatting.
    && poetry install --no-interaction --no-ansi

# Copy the rest of the app
COPY . .

# Expose port
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]