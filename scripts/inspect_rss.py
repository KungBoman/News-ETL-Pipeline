import pprint
import sys

import feedparser  # type: ignore[import-untyped]


def main() -> None:
    url = sys.argv[1]

    feed = feedparser.parse(url)

    print(f"Feed title: {feed.feed.get('title')}")
    print(f"Entries: {len(feed.entries)}")

    if not feed.entries:
        raise SystemExit("No entries found")

    entry = feed.entries[0]

    print("\nAvailable fields:")
    for field in entry:
        print(f"- {field}")

    print("\nFirst article:")
    for key, value in entry.items():
        print(f"\n- {key}:\n{value}")

    print("\nCopy-paste entry:")
    pprint.pprint(dict(entry), sort_dicts=False)


if __name__ == "__main__":
    main()
