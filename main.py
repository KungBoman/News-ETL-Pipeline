from src.pipeline import run_pipeline


def main() -> None:
    stats = run_pipeline()

    print(f"Extracted: {stats['extracted']} articles")
    print(f"Transformed: {stats['transformed']} articles")
    print(f"Valid: {stats['valid']} articles")
    print(f"Loaded: {stats['loaded']} articles")


if __name__ == "__main__":
    main()
