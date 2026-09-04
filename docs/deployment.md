# Deployment

The project uses Docker to provide a reproducible runtime environment for the API and PostgreSQL.

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

The API is then available at:

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

## CI/CD Deployment Flow

The project uses GitHub Actions for automated testing and delivery.

Normal development:

```text
Pull Request
     ↓
    CI
     ↓
   Tests
```

Changes merged to `main`:

```text
Push to main
     ↓
    CI
     ↓
   Tests
     ↓
Docker build
```

Creating a version tag:

```text
Create v* tag
     ↓
Release workflow
     ↓
   Tests
     ↓
Docker build
     ↓
Push image to GHCR
     ↓
GitHub Release
```

The release workflow therefore only publishes an image after the test suite has passed.

## Versioned Releases

Releases are created using Git tags following the versioning convention:

```text
vMAJOR.MINOR.PATCH
```

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The tag triggers the release workflow.

Version tags are immutable references to specific Git commits, which makes it possible to identify exactly which version of the source code produced a Docker image or release artifact.

## Production Deployment

The current project focuses on containerization and automated delivery rather than deployment to a specific cloud provider.

The Docker image published to GHCR can be used as the deployment artifact for a future hosting environment.

This keeps the application deployment-independent and allows the same image to be deployed to different container platforms.