#!/usr/bin/env python3
"""
Convert LCOV to SonarQube Generic Test Coverage XML format.

Usage:
  python3 scripts/lcov_to_sonar.py cover/lcov.info cover/sonar-generic-coverage.xml

The output format is:
<coverage version="1">
  <file path="lib/...">
    <lineToCover lineNumber="N" covered="true|false"/>
  </file>
</coverage>
"""

import os
import sys
import xml.etree.ElementTree as ET


def parse_lcov(lcov_path: str):
    files = {}
    current = None
    try:
        with open(lcov_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if line.startswith("SF:"):
                    path = line[3:]
                    current = path
                    files.setdefault(current, {})
                elif line.startswith("DA:") and current:
                    # DA:<line number>,<execution count>[,<checksum>]
                    try:
                        payload = line[3:]
                        parts = payload.split(",")
                        ln = int(parts[0])
                        hits = int(parts[1])
                        files[current][ln] = hits > 0
                    except Exception:
                        # ignore malformed lines
                        pass
                elif line == "end_of_record":
                    current = None
    except FileNotFoundError:
        print(f"ERROR: LCOV file not found: {lcov_path}", file=sys.stderr)
        sys.exit(1)
    return files


def to_sonar_xml(files_hits: dict, cwd: str):
    cov = ET.Element("coverage", {"version": "1"})

    for path, lines in sorted(files_hits.items()):
        # Make path relative to repo root to match sonar.sources
        rel = os.path.relpath(path, cwd)
        # Only include source files inside the project (e.g., lib/)
        if rel.startswith(".."):
            # Try to find a suffix that starts with lib/
            lib_index = path.find(os.sep + "lib" + os.sep)
            if lib_index != -1:
                rel = path[lib_index + 1 :]
        if not (rel.startswith("lib/") or rel.startswith("apps/") or rel.endswith(".ex")):
            # Skip files outside Elixir sources
            continue

        file_el = ET.SubElement(cov, "file", {"path": rel})
        for ln in sorted(lines.keys()):
            covered = lines[ln]
            ET.SubElement(
                file_el,
                "lineToCover",
                {"lineNumber": str(ln), "covered": "true" if covered else "false"},
            )

    return cov


def write_xml(root: ET.Element, out_path: str):
    tree = ET.ElementTree(root)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)


def main():
    if len(sys.argv) != 3:
        print("Usage: lcov_to_sonar.py <lcov.info> <out.xml>")
        sys.exit(2)
    lcov_path = sys.argv[1]
    out_path = sys.argv[2]

    files_hits = parse_lcov(lcov_path)
    root = to_sonar_xml(files_hits, os.getcwd())
    write_xml(root, out_path)
    print(f"Wrote Sonar generic coverage XML to {out_path}")


if __name__ == "__main__":
    main()
