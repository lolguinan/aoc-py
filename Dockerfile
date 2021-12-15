FROM python:3.10-alpine

WORKDIR /app

COPY pyproject.toml .
COPY setup.cfg .
COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -U pip \
    && pip install -r requirements.txt \
    && pip install -r requirements-dev.txt

COPY src/ src/
COPY tests/ tests/
COPY inputs/ inputs/
COPY run.py .

RUN pip install -e .

ENTRYPOINT ["python3", "run.py"]
