FROM python:3.10 AS deps

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && /root/.local/bin/poetry config virtualenvs.create false

# Copy Poetry data
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./

# Generate requirements list
RUN /root/.local/bin/poetry export -o requirements.txt


FROM python:3.10

# Install requirements
COPY --from=deps /usr/src/app/requirements.txt /requirements.txt
RUN pip --disable-pip-version-check install --no-cache-dir -r /requirements.txt

# Set up app
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY smtprelay.py ./

EXPOSE 2525
CMD ["python3", "smtprelay.py"]
