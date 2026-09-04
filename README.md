# Swedish News ETL Pipeline
A Python ETL pipeline that collects Swedish news articles from RSS feeds, validates and deduplicates the data, stores it in a database, and runs automated tests with GitHub Actions.

## Architecture
RSS Feeds  
- Extract  
- Transform  
- Validate  
- Deduplicate  
- PostgreSQL  

## Features
- Extracts news from multiple Swedish RSS sources
- Cleans and standardizes article data
- Enriches articles with a politics-related flag
- Deduplicates articles based on URL
- Validates required fields
- Loads data into PostgreSQL
- Error handling, logging and transaction rollback
- Automated tests with pytest
- GitHub Actions CI
- Scheduled pipeline execution
- Versioned GitHub Releases

## Tech Stack

- Python
- PostgreSQL
- Docker
- pytest
- GitHub Actions

## Setup

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Configure environment variables
Create a `.env` file:
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=news
DB_USER=news_user
DB_PASSWORD=news_password
```

### 3. Create the database schema
```bash
docker exec -i news-etl-postgres psql -U news_user -d news < sql/schema.sql
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the pipeline
```bash
python main.py
```

### 6. Run tests
```bash
pytest
```

### CI/CD
GitHub Actions automatically runs the test suite on pushes and pull requests.

The pipeline can also be triggered on a schedule and runs against a temporary PostgreSQL service.

Version tags trigger a release workflow that:

1. Runs the tests
2. Builds a project artifact
3. Creates a GitHub Release

Example:
```bash
git tag v1.0.0
git push origin v1.0.0
```

### Docker

Check that Docker is installed:
```bash
docker --version
docker compose version
```

Start the PostgreSQL container:
```bash
docker compose up -d
```

Connect to the database:
```bash
docker exec -it news-etl-postgres psql -U news_user -d news
```
