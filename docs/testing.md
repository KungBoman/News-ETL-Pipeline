# Testing

The project uses pytest for automated testing.

The test suite is divided into different levels to verify both individual components and the interaction between components.

## Test Structure

```text id="3czj6d"
tests/
├── test_helpers.py
├── test_common_util.py
│
├── test_extract.py
├── test_transform.py
├── test_validate.py
├── test_load.py
│
├── test_api.py
├── test_repository_articles.py
├── test_repository_pipeline_runs.py
└── test_api_integration.py
```

## Unit Tests

Unit tests verify individual functions and components in isolation.

Examples include:

- RSS extraction
- Data cleaning
- Data enrichment
- Deduplication
- Validation
- Database loading logic
- API endpoint behavior

External dependencies such as database connections are mocked where appropriate.

This keeps unit tests fast and makes it possible to test specific behaviors without depending on external systems.

## Repository Tests

Repository tests verify SQL queries against a real PostgreSQL database.

These tests cover functionality such as:

- Fetching articles
- Pagination
- Filtering by source
- Filtering by politics-related status
- Fetching an article by ID
- Handling missing articles
- Creating and updating pipeline runs
- Fetching pipeline run history

A dedicated PostgreSQL test database is used so that repository tests do not affect the development database.

## API Integration Tests

Integration tests verify the API together with the real PostgreSQL test database.

For example, an API request such as:

```text
GET /articles/?source=SVT
```

is executed against the test database and the returned JSON response is verified.

These tests provide confidence that the API, repository layer, database connection, SQL queries, and response models work together correctly.

## Test Database

The test environment uses a separate PostgreSQL instance:

```text
Host: localhost
Port: 5433
Database: news_test
```

The development database uses port `5432`.

The test database is prepared before integration tests by:

1. Creating the required database tables
2. Clearing existing test data
3. Inserting known test data
4. Running the tests
5. Cleaning up the test data

This gives the tests a predictable starting state without affecting development data.

## Test Coverage

The project uses `pytest-cov` to measure test coverage.

Coverage is reported for the `src` package:

```bash
pytest --cov=src --cov-report=term-missing
```

The CI workflow enforces a minimum coverage threshold.

Coverage below 70% fails the CI job, while coverage below 80% produces a warning.

The current test suite provides approximately 99% coverage.

The goal is not to achieve 100% coverage at any cost, but to ensure that important application behavior and failure paths are tested.

## Running Tests

Run the complete test suite with:

```bash
pytest
```

Tests can also be run against a specific file:

```bash
pytest tests/test_transform.py
```

Or a specific test:

```bash
pytest tests/test_transform.py::test_clean_article
```

## Local CI

The project includes a local CI script that runs the main quality checks before changes are pushed to GitHub.

Run:

```bash
python ci.py
```

This runs:

1. Ruff
2. Mypy
3. Pytest

To also verify the Docker environment:

```bash
python ci.py --docker
```

This additionally builds the Docker image, starts the services, and verifies that the API health endpoint becomes available.

## CI Testing

GitHub Actions runs the complete test suite automatically.

The CI environment starts a temporary PostgreSQL service and provides the test database configuration through environment variables.

This means that the same database-dependent tests can be executed in CI without relying on an external database.

The release workflow also runs the test suite before publishing the Docker image or creating the release artifacts.

## Testing Strategy

The project intentionally uses both mocked and real database tests.

Mock-based tests are useful for fast and isolated unit testing.

Real PostgreSQL tests are used where actual database behavior matters, particularly for SQL queries and API/database integration.

This provides a balance between test speed and confidence in the complete system.