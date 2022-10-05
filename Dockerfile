FROM python:3.10

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && /root/.local/bin/poetry config virtualenvs.create false

# Set up app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock smtprelay.py README.md ./
RUN /root/.local/bin/poetry install --no-interaction --no-dev && rm -rf /root/.cache

EXPOSE 2525
CMD ["python3", "smtprelay.py"]
