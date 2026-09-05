import subprocess


def main() -> None:
    with open("sql/schema.sql", encoding="utf-8") as schema_file:
        subprocess.run(
            [
                "docker",
                "exec",
                "-i",
                "news-etl-postgres",
                "psql",
                "-U",
                "news_user",
                "-d",
                "news",
            ],
            stdin=schema_file,
            check=True,
        )


if __name__ == "__main__":
    main()
