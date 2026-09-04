# Testing

The project uses pytest for automated testing.

The test suite is divided into different levels to verify both individual components and the interaction between components.

## Test Structure

```text
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
├── test_repository.py
└── test_api_integration.py
```

## Unit Tests

Unit tests verify individual functions and components in isolation.

Examples include:

- RSS extraction
- Data cleaning
- Data enrichment
- Validation
- Database loading logic
- API endpoint behavior

External dependencies such as database connections are mocked where appropriate.

This keeps unit tests fast and makes it possible to test specific behaviors without depending on external systems.

## Repository Tests

Repository tests verify the SQL queries against a real PostgreSQL database.

These tests cover functionality such as:

- Fetching articles
- Pagination
- Filtering by source
- Filtering by politics-related status
- Fetching an article by ID
- Handling missing articles

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

1. Creating the `articles` table if it does not exist
2. Clearing existing data
3. Inserting known test data
4. Running the tests
5. Clearing the data after the test

This gives the tests a predictable starting state.

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

## CI Testing

GitHub Actions runs the complete test suite automatically.

The CI environment starts a temporary PostgreSQL service and provides the test database configuration through environment variables.

This means that the same database-dependent tests that run locally are also executed in CI.

The release workflow also runs the test suite before creating a release or publishing the Docker image.

## Testing Strategy

The project intentionally uses both mocked and real database tests.

Mock-based tests are useful for fast and isolated unit testing.

Real PostgreSQL tests are used where the actual database behavior matters, particularly for SQL queries and API/database integration.

This provides a balance between test speed and confidence in the complete system.