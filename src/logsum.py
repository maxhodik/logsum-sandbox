import argparse
import csv
import sys
from collections import defaultdict


def parse_event_row(row):
    """Normalise and extract fields from a single CSV row."""
    timestamp = row.get("timestamp", "").strip()
    level = row.get("level", "").strip() or "UNKNOWN"
    service = row.get("service", "").strip()
    return timestamp, level, service


def main():
    parser = argparse.ArgumentParser(description="Summarise synthetic event logs.")
    parser.add_argument("input", help="Path to input events.csv")
    parser.add_argument("output", help="Path to output summary.csv")
    parser.add_argument(
        "--min-count",
        type=int,
        default=0,
        help="Minimum event count threshold to include group in output",
    )
    args = parser.parse_args()

    groups = defaultdict(lambda: {"count": 0, "first_seen": None, "last_seen": None})

    try:
        with open(args.input, mode="r", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                timestamp, level, service = parse_event_row(row)
                if not timestamp and not service:
                    continue

                key = (service, level)
                g = groups[key]
                g["count"] += 1

                if not g["first_seen"] or timestamp < g["first_seen"]:
                    g["first_seen"] = timestamp
                if not g["last_seen"] or timestamp > g["last_seen"]:
                    g["last_seen"] = timestamp

        with open(args.output, mode="w", encoding="utf-8", newline="") as outfile:
            fieldnames = ["service", "level", "count", "first_seen", "last_seen"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, g in groups.items():
                if g["count"] < args.min_count:
                    continue  # Apply min-count filter
                writer.writerow({
                    "service": key[0],
                    "level": key[1],
                    "count": g["count"],
                    "first_seen": g["first_seen"],
                    "last_seen": g["last_seen"],
                })
        print(f"Summary successfully written to {args.output}")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()