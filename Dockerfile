FROM python:3.13.3-slim

# 1) set workdir
WORKDIR /app

# 2) upgrade pip + build tooling
RUN pip install --upgrade pip setuptools wheel

# 3) copy only the pyproject
COPY pyproject.toml ./

# 4) install the project (pyproject.toml)
RUN pip install --no-cache-dir .

# 5) copying the source
COPY . .

# 6) expose & start
EXPOSE 5000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "run:app"]