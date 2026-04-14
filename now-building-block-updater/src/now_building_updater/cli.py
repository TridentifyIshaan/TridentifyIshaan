from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .generator import (
    END_MARKER,
    START_MARKER,
    apply_readme_update,
    build_entries,
    render_block,
)
from .github_api import GitHubApiError, GitHubClient


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Insert or monthly-update a managed Now Building block in a README from "
            "GitHub repository activity."
        )
    )
    parser.add_argument("--username", required=True, help="GitHub username to analyze")
    parser.add_argument(
        "--readme-path",
        default="README.md",
        help="Path to README file to update (default: README.md)",
    )
    parser.add_argument(
        "--months",
        type=int,
        default=3,
        help="How many recent months to include (default: 3)",
    )
    parser.add_argument(
        "--rows-per-month",
        type=int,
        default=2,
        help=(
            "How many separate rows to generate per month. "
            "Use values >1 to list multiple tracks in the same month (default: 2)"
        ),
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help=(
            "Include private repos when token has access. For full private coverage, "
            "token should belong to --username with owner repo access."
        ),
    )
    parser.add_argument(
        "--include-forks",
        action="store_true",
        help="Include fork repositories (default: disabled)",
    )
    parser.add_argument(
        "--include-archived",
        action="store_true",
        help="Include archived repositories (default: disabled)",
    )
    parser.add_argument(
        "--note",
        default="♻️ Updating this block every month!.",
        help="Footer note shown below the table",
    )
    parser.add_argument(
        "--token-env",
        default="GITHUB_TOKEN",
        help="Environment variable name containing GitHub token (default: GITHUB_TOKEN)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print updated block to stdout without modifying files",
    )
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args(sys.argv[1:])

    token = os.getenv(args.token_env)
    github = GitHubClient(token=token)

    try:
        entries = build_entries(
            github=github,
            username=args.username,
            months=args.months,
            rows_per_month=args.rows_per_month,
            include_private=args.include_private,
            include_forks=args.include_forks,
            include_archived=args.include_archived,
        )
    except GitHubApiError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    block = render_block(entries=entries, note=args.note)

    if args.dry_run:
        print(f"{START_MARKER}\n{block}\n{END_MARKER}")
        return 0

    readme_path = Path(args.readme_path)
    if not readme_path.exists():
        print(f"error: README path does not exist: {readme_path}", file=sys.stderr)
        return 2

    readme_before = readme_path.read_text(encoding="utf-8")
    readme_after, replaced_existing = apply_readme_update(readme_before, block)

    if readme_after == readme_before:
        print("No changes needed.")
        return 0

    readme_path.write_text(readme_after, encoding="utf-8")
    if replaced_existing:
        print("Updated existing managed Now Building block.")
    else:
        print("Inserted managed Now Building block.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
