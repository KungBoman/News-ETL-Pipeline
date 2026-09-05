import argparse
import subprocess
import time
from http.client import RemoteDisconnected
from urllib.error import URLError
from urllib.request import urlopen


def run_step(
    name: str,
    command: list[str],
    quiet: bool = False,
    message: str | None = None,
) -> None:
    print(f"\n=== {name} ===")

    if message:
        print(message)

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.DEVNULL if quiet else None,
    )

    print(f"✓ {name} passed")


def wait_for_api(url: str, timeout: int = 30) -> None:
    print("\n=== Waiting for API ===")

    start = time.time()

    while time.time() - start < timeout:
        try:
            with urlopen(url, timeout=5):
                print("✓ API is running")
                return
        except (URLError, RemoteDisconnected):
            time.sleep(1)

    raise RuntimeError(f"API did not become available within {timeout} seconds")


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

    if args.docker:
        run_step(
            "Docker",
            ["docker", "compose", "up", "-d", "--build"],
            quiet=True,
            message="Building and starting containers...",
        )

        wait_for_api("http://localhost:8000/health")

        print("Swagger: http://localhost:8000/docs\n")

    run_step("Tests", ["pytest", "-q"])


if __name__ == "__main__":
    main()
