import argparse
import subprocess


def run_step(name: str, command: list[str]) -> None:
    print(f"\n=== {name} ===")

    subprocess.run(command, check=True)

    print(f"✓ {name} passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--docker",
        action="store_true",
        help="Build and start Docker services",
    )
    args = parser.parse_args()

    run_step("Ruff", ["ruff", "check", "."])
    run_step("Mypy src", ["mypy", "src"])
    run_step("Mypy tests", ["mypy", "tests"])
    run_step("Tests", ["pytest", "-q"])

    if args.docker:
        run_step(
            "Docker",
            ["docker", "compose", "up", "-d", "--build"],
        )
        print("\nSwagger: http://localhost:8000/docs")


if __name__ == "__main__":
    main()
