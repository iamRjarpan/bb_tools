#!/usr/bin/env python3

import sys
import re

def normalize_path(path):
    """Replaces numeric parts of a path with a placeholder."""
    # This regex finds and replaces any sequence of one or more digits
    return re.sub(r'\d+', '{id}', path)

def main():
    """
    Reads lines from stdin, filters for unique endpoint paths
    (ignoring differences in numeric IDs), and prints one representative
    endpoint for each unique path.
    """
    seen_normalized_paths = set()

    try:
        for line in sys.stdin:
            original_path = line.strip()
            if not original_path:
                continue

            normalized = normalize_path(original_path)

            if normalized not in seen_normalized_paths:
                seen_normalized_paths.add(normalized)
                print(original_path)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        sys.exit(0)

if __name__ == "__main__":
    main()
