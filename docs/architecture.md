# Architecture

## Overview

Swedish News ETL Pipeline is a Python-based ETL system that collects Swedish news articles from multiple RSS feeds, processes and validates the data, stores the results in PostgreSQL, and exposes the data through a REST API.

The project is designed as a small but complete data engineering system covering ingestion, transformation, validation, persistence, API access, testing, containerization, and CI/CD.

## System Architecture

```mermaid
flowchart TD
    A[RSS Feeds] --> B[Extract]
    B --> C[Transform]
    C --> D[Deduplicate]
    D --> E[Validate]
    E --> F[PostgreSQL]
    F --> G[REST API]
    G --> H[Clients]
```

The ETL pipeline processes articles through a sequence of stages:

1. Extract data from RSS feeds
2. Clean and transform the articles
3. Enrich the article data
4. Deduplicate articles
5. Validate required fields
6. Store valid articles in PostgreSQL

Each pipeline execution is also tracked in the `pipeline_runs` table.

## Extract

The extract stage collects articles from multiple Swedish RSS sources.

Currently supported sources include:

- SVT
- Aftonbladet
- Expressen
- Svenska Dagbladet

Each RSS entry is converted into a common article structure defined using Python's `TypedDict`.

The extract stage also converts publication timestamps into timezone-aware `datetime` objects.

If an individual RSS source fails, the pipeline logs the error and continues processing the remaining sources.

## Transform

The transform stage prepares the extracted data before validation and loading.

It consists of several steps.

### Clean

String fields are stripped of unnecessary whitespace and empty strings are converted to `None`.

### Standardize

The standardization stage provides a common internal structure for article data.

This allows articles from different RSS sources to pass through the same downstream pipeline.

### Enrich

Articles are enriched with an `is_politics_related` flag based on keyword matching in the article title and summary.

### Deduplicate

Articles are deduplicated using their URL.

The URL is also defined as a unique constraint in PostgreSQL, providing a second layer of protection against duplicate records.

## Validate

The validation stage checks that required fields are present before data is loaded into PostgreSQL.

Required fields are:

- `source`
- `title`
- `url`
- `published_at`

Invalid articles are excluded from the load stage.

## PostgreSQL

PostgreSQL is the persistent storage layer.

The database contains two main tables:

### `articles`

Stores the transformed and validated news articles.

The table includes:

- Source and article metadata
- Publication timestamp
- Article URL
- Enrichment information
- A unique constraint on the article URL

Article inserts use PostgreSQL's `ON CONFLICT` handling to safely skip duplicates.

### `pipeline_runs`

Stores information about individual ETL executions.

Each run records:

- Start time
- Finish time
- Status
- Number of extracted articles
- Number of transformed articles
- Number of valid articles
- Number of loaded articles
- Error information when applicable

This provides basic pipeline observability and makes failed executions visible through the API.

## Database Transactions

Database writes are performed inside transactions.

During article loading, all inserts are part of the same transaction. If an error occurs, the transaction is rolled back.

Pipeline run metadata is committed separately so that the final status of the pipeline can be recorded even when the article load fails.

## REST API

The project exposes the stored data through a FastAPI REST API.

Current endpoints include:

- `GET /articles/` — list articles
- `GET /articles/{id}` — fetch an article by ID
- `GET /pipeline-runs/` — list pipeline executions
- `GET /health` — check API and database health

The article endpoint supports:

- Pagination using `limit` and `offset`
- Filtering by source
- Filtering by `is_politics_related`

FastAPI also provides interactive OpenAPI/Swagger documentation.

## Repository Layer

Database queries are separated from the API and pipeline logic through repository modules.

```text
src/
├── repository/
│   ├── articles.py
│   └── pipeline_runs.py
```

The repository layer is responsible for database queries, while routers handle HTTP requests and responses.

This separation keeps database access isolated and makes the repository functions easier to test independently.

## Docker

Docker is used to provide a reproducible runtime environment.

The Docker Compose setup contains:

- PostgreSQL development database
- PostgreSQL test database
- FastAPI application

The API runs with Uvicorn inside its own container and communicates with PostgreSQL through the Docker Compose service name.

The test database runs separately from the development database to prevent tests from modifying development data.

## Testing

The project uses pytest with multiple testing levels:

- Unit tests for individual functions
- Repository tests against a real PostgreSQL test database
- API tests
- Integration tests covering the API together with PostgreSQL
- Pipeline tests covering pipeline execution and run tracking

The test suite also uses coverage reporting to detect regressions in tested code.

More details are documented in `docs/testing.md`.

## CI/CD

GitHub Actions automates the project's quality checks, scheduled ETL execution, Docker builds, and releases.

The three workflows are:

- `ci.yml` — continuous integration
- `pipeline.yml` — scheduled ETL execution
- `release.yml` — versioned releases

The CI/CD architecture is documented separately in `docs/ci-cd.md`.

## Design Decisions

### RSS instead of direct API integrations

RSS provides a simple and standardized way of collecting articles from multiple news sources without requiring separate API integrations for every source.

### TypedDict for article data

`TypedDict` provides static type checking while keeping article data as normal Python dictionaries.

This allows the same article structure to be passed between the different ETL stages while still benefiting from mypy type checking.

### PostgreSQL

PostgreSQL provides reliable persistent storage, constraints, transactions, and SQL querying capabilities.

It also provides a realistic relational database layer for development and integration testing.

### Separate test database

The test suite uses a dedicated PostgreSQL database running on a separate port.

This prevents tests from modifying development data.

### Repository layer

Database queries are separated from the API and pipeline logic.

This keeps responsibilities clear and makes database operations easier to test independently.

### FastAPI

FastAPI provides a lightweight REST API with automatic request validation and interactive OpenAPI/Swagger documentation.

### Docker

Docker makes the application and its dependencies reproducible and allows the API and databases to run consistently across environments.