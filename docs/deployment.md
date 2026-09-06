# Deployment

The project uses Docker to provide a reproducible runtime environment for the API and PostgreSQL.

Production deployment uses Render for the API and PostgreSQL, while GitHub Actions handles automated ETL execution.

## Local Environment

The Docker Compose setup contains three services:

```text
docker-compose.yml
│
├── postgres
│   └── Development database
│
├── postgres-test
│   └── Test database
│
└── api
    └── FastAPI application
```

The development PostgreSQL database is exposed on port `5432`, while the test database is exposed on port `5433`.

The API is exposed on port `8000`.

## Start the Application

Start all services with:

```bash
docker compose up -d
```

Check the running containers:

```bash
docker compose ps
```

The API is available at:

```text
http://localhost:8000
```

Interactive Swagger documentation is available at:

```text
http://localhost:8000/docs
```

## Database

The PostgreSQL database is initialized using the schema in:

```text
sql/schema.sql
```

The schema can be applied with:

```bash
docker exec -i news-etl-postgres psql -U news_user -d news < sql/schema.sql
```

The API connects to PostgreSQL using the Docker Compose service name:

```text
DB_HOST=postgres
```

Inside the Docker network, `postgres` resolves to the PostgreSQL container.

## Docker Image

The API is built using the root `Dockerfile`.

The image:

1. Uses Python 3.12
2. Installs the Python dependencies
3. Copies the application code
4. Exposes port `8000`
5. Starts Uvicorn with the FastAPI application

The application starts with:

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

## GitHub Container Registry

Release builds publish the API Docker image to GitHub Container Registry (GHCR).

Images are tagged using both the Git version tag and `latest`.

For example:

```text
ghcr.io/kungboman/news-etl-api:v1.0.2
ghcr.io/kungboman/news-etl-api:latest
```

This makes it possible to run either a specific version or the latest release.

## CI/CD

GitHub Actions is used for automated testing, Docker builds, scheduled pipeline execution, and releases.

### Continuous Integration

Pull requests and pushes to `main` run the CI workflow.

The workflow:

1. Starts a temporary PostgreSQL test database
2. Installs the Python dependencies
3. Runs Ruff
4. Runs mypy
5. Runs the test suite with coverage
6. Builds the Docker image

### Scheduled Pipeline

The ETL pipeline runs automatically on a daily schedule using GitHub Actions.

The pipeline is split into two stages.

#### Pipeline Test

The first job:

1. Starts a temporary PostgreSQL database
2. Applies the database schema
3. Runs the ETL pipeline against the test database

If this job fails, the production job does not run.

#### Production Pipeline

After the test job succeeds, the production job:

1. Installs the Python dependencies
2. Connects to the production PostgreSQL database on Render
3. Runs the ETL pipeline
4. Stores the resulting articles in the production database
5. Records the pipeline execution in `pipeline_runs`

The workflow can also be triggered manually.

## Production Environment

The production environment consists of:

```text
GitHub Actions
      │
      │ scheduled ETL
      ▼
Production ETL
      │
      ▼
Render PostgreSQL
      ▲
      │
Render Web Service
      │
      ▼
    REST API
```

The FastAPI application is deployed as a Render Web Service.

The production database is hosted using Render PostgreSQL.

The production API is available at:

```text
https://news-etl-api.onrender.com
```

Swagger documentation:

```text
https://news-etl-api.onrender.com/docs
```

The production database is accessed by GitHub Actions using Render's external PostgreSQL connection.

The Render Web Service uses the internal database connection available within the Render environment.

## Production Database Schema

The production PostgreSQL schema is created separately using:

```text
sql/schema.sql
```

Once the schema has been created, scheduled ETL executions only load and update data. The production GitHub Actions job does not recreate the schema on every run.

## Releases

Creating a Git tag following the `vMAJOR.MINOR.PATCH` format triggers the release workflow.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow:

1. Runs the test suite
2. Builds the Docker image
3. Pushes the versioned image to GHCR
4. Updates the `latest` image tag
5. Creates a GitHub Release
6. Publishes the source artifact

The release workflow only publishes artifacts after the tests have passed.

## Local CI

The project also includes `scripts/ci.py` for running the core quality checks locally before pushing changes.

Run:

```bash
python scripts/ci.py
```

This runs:

1. Ruff
2. Mypy for `src`
3. Mypy for `tests`
4. Pytest

To also verify the Docker environment:

```bash
python scripts/ci.py --docker
```

This additionally:

1. Builds the Docker image
2. Starts the Docker Compose services
3. Waits for the API health endpoint
4. Prints the Swagger URL

This provides a local verification step before changes are pushed to GitHub.