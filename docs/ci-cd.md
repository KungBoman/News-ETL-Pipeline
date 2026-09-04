# CI/CD

The project uses GitHub Actions to automate testing, pipeline execution, Docker builds, and releases.

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

## Continuous Integration

The CI workflow runs automatically for:

- Pull requests
- Pushes to `main`

It can also be triggered manually.

The workflow:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Starts a temporary PostgreSQL test service
5. Runs the complete pytest suite
6. Builds the Docker image

This ensures that changes are tested before they are merged and that the application can be containerized successfully.

## Scheduled Pipeline

The pipeline workflow runs the ETL pipeline automatically on a schedule.

It can also be triggered manually.

The workflow:

1. Starts a temporary PostgreSQL database
2. Installs dependencies
3. Creates the database schema
4. Runs the ETL pipeline

The scheduled workflow uses the same pipeline entry point as local execution:

```bash
python main.py
```

This keeps the scheduled execution consistent with the local application.

## Release Workflow

The release workflow is triggered when a version tag is created.

Only tags starting with `v` are considered releases.

Example:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow:

1. Runs the test suite
2. Builds the Docker image
3. Logs in to GitHub Container Registry
4. Publishes the Docker image to GHCR
5. Creates a GitHub Release
6. Attaches the project artifact to the release

## Docker Image Tags

Each release produces two Docker image tags:

```text
ghcr.io/<owner>/news-etl-api:v1.0.0
ghcr.io/<owner>/news-etl-api:latest
```

The version-specific tag makes it possible to run a known release, while `latest` points to the most recent release.

## Test Database in CI

Database-dependent tests use a temporary PostgreSQL service provided by GitHub Actions.

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

## Workflow Separation

The workflows are intentionally separated by responsibility:

```text
Pull Request
     ↓
    CI
     ↓
   Tests

Push to main
     ↓
    CI
     ↓
   Tests → Docker build

Scheduled execution
     ↓
  Pipeline
     ↓
    ETL → PostgreSQL

Version tag
     ↓
  Release
     ↓
   Tests
     ↓
   Docker → GHCR
     ↓
GitHub Release
```

This separation keeps the CI workflow focused on code quality while the release workflow handles versioned delivery.