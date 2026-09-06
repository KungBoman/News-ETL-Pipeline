# CI/CD

The project uses GitHub Actions to automate code quality checks, testing, ETL execution, Docker builds, and releases.

## Workflows

The project contains three GitHub Actions workflows:

```text
.github/
└── workflows/
    ├── ci.yml
    ├── pipeline.yml
    └── release.yml
```

Each workflow has a separate responsibility.

| Workflow | Trigger | Responsibility |
|---|---|---|
| `ci.yml` | Pull requests, pushes to `main`, manual | Quality checks, tests, Docker build |
| `pipeline.yml` | Scheduled, manual | Test and production ETL execution |
| `release.yml` | Version tags | Test, build, publish Docker image, create release |

## Continuous Integration

The CI workflow runs automatically for:

- Pull requests
- Pushes to `main`

It can also be triggered manually.

The workflow:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs dependencies
4. Starts a temporary PostgreSQL test service
5. Runs Ruff
6. Runs mypy
7. Runs pytest with coverage
8. Builds the Docker image

Database-dependent tests run against the temporary PostgreSQL service.

This ensures that changes pass the quality checks and test suite before they are merged.

## Scheduled Pipeline

The pipeline workflow runs the ETL process automatically once per day.

It can also be triggered manually.

The workflow is split into two jobs:

```text
Scheduled / Manual
       ↓
 Pipeline Test
       ↓
   ETL against
 temporary PostgreSQL
       ↓
   succeeds?
      / \
    yes  no
     ↓    ↓
Production  Stop
 Pipeline
     ↓
Render PostgreSQL
```

### Pipeline Test

The first job runs the ETL pipeline against a temporary PostgreSQL database provided by GitHub Actions.

It:

1. Starts PostgreSQL
2. Installs dependencies
3. Creates the database schema
4. Runs the ETL pipeline

The same `main.py` entry point is used for the test execution as for local execution.

If the test job fails, the production job is not executed.

### Production Pipeline

The production job only runs after the pipeline test succeeds.

It:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs dependencies
4. Connects to the production PostgreSQL database on Render
5. Runs `python main.py`
6. Loads the processed articles into the production database
7. Records the pipeline execution in `pipeline_runs`

Production database credentials are stored as GitHub Actions secrets.

This provides a basic deployment safety mechanism where the production ETL pipeline is only executed after the test pipeline has completed successfully.

## Release Workflow

The release workflow is triggered when a version tag is created.

Only tags starting with `v` are considered releases.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow:

1. Checks out the tagged version
2. Starts a temporary PostgreSQL test service
3. Installs dependencies
4. Runs the test suite
5. Builds the Docker image
6. Logs in to GitHub Container Registry
7. Publishes the Docker image to GHCR
8. Creates a GitHub Release
9. Attaches the project artifact to the release

The release workflow only publishes artifacts after the tests have passed.

## Docker Image Tags

Each release produces two Docker image tags:

```text
ghcr.io/<owner>/news-etl-api:v1.0.0
ghcr.io/<owner>/news-etl-api:latest
```

The version-specific tag makes it possible to run a known release, while `latest` points to the most recent release.

## Test Database in CI

Database-dependent tests use temporary PostgreSQL services provided by GitHub Actions.

The CI environment uses:

```text
DB_HOST=localhost
DB_PORT=5433
DB_NAME=news_test
DB_USER=news_user
DB_PASSWORD=news_password
```

The test database is separate from the development database.

This allows repository and API integration tests to run against a real PostgreSQL instance without depending on an external database.

The scheduled pipeline also uses a temporary PostgreSQL database for its pipeline test job before running the production ETL.

## Production Database

The production ETL pipeline connects to the Render PostgreSQL database using credentials stored in GitHub Actions Secrets.

GitHub Actions connects using Render's external PostgreSQL connection.

The deployed FastAPI application uses the Render internal database connection.

This keeps production database credentials out of the source code and allows the scheduled pipeline to load data into the production database securely.

## Workflow Separation

The workflows are intentionally separated by responsibility:

```text
Pull Request
     ↓
    CI
     ↓
Ruff → Mypy → Pytest → Docker build

Push to main
     ↓
    CI
     ↓
Ruff → Mypy → Pytest → Docker build

Scheduled / Manual
     ↓
 Pipeline
     ↓
Pipeline Test
     ↓
Temporary PostgreSQL
     ↓
    success
     ↓
Production Pipeline
     ↓
Render PostgreSQL

Version tag
     ↓
  Release
     ↓
   Tests
     ↓
 Docker build
     ↓
   GHCR
     ↓
GitHub Release
```

This separation keeps continuous integration, scheduled data processing, and release delivery independent from each other while still providing a controlled path to the production database.