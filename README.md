# News-ETL-Pipeline
A Python ETL pipeline that collects Swedish news articles from RSS feeds, validates and deduplicates the data, stores it in a database, and runs automated tests with GitHub Actions.

### Docker
```powershell
wsl --status
wsl --version
```
Install Docker Desktop
```bash
docker --version
docker compose version
docker compose up -d
```

Run SQL-file on database in container, then verify
```powershell
Get-Content .\sql\schema.sql | docker exec -i news-etl-postgres psql -U news_user -d news
docker exec -it news-etl-postgres psql -U news_user -d news
```
