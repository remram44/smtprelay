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

# Set up user
RUN mkdir -p /usr/src/app/home && \
    useradd -d /usr/src/app/home -s /usr/sbin/nologin -u 998 appuser && \
    chown appuser /usr/src/app/home

ENV PYTHONFAULTHANDLER=1

USER 998
EXPOSE 2525
CMD ["python3", "smtprelay.py"]
