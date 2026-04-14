from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Sequence, Tuple

from .github_api import GitHubClient, Repo, iso_month_range

START_MARKER = "<!-- NOW_BUILDING:START -->"
END_MARKER = "<!-- NOW_BUILDING:END -->"
DEFAULT_HEADER = "## Now Building"


@dataclass
class MonthEntry:
    year: int
    month: int
    build_track: str
    shipping_goal: str


def build_entries(
    github: GitHubClient,
    username: str,
    months: int,
    include_private: bool,
    include_forks: bool,
    include_archived: bool,
) -> List[MonthEntry]:
    now = datetime.now(timezone.utc)
    month_pairs = _recent_months(now.year, now.month, months)

    repos = github.list_repos_for_user(username=username, include_private=include_private)
    repos = [
        repo
        for repo in repos
        if (include_forks or not repo.fork) and (include_archived or not repo.archived)
    ]

    entries: List[MonthEntry] = []
    for year, month in month_pairs:
        since_iso, until_iso = iso_month_range(year, month)
        repo_scores: List[Tuple[Repo, int]] = []

        for repo in repos:
            commits = github.count_commits(repo.owner, repo.name, since_iso, until_iso)
            if commits <= 0:
                continue
            repo_scores.append((repo, commits))

        repo_scores.sort(key=lambda item: item[1], reverse=True)
        top_repos = [item[0] for item in repo_scores[:2]]

        build_track = _build_track(top_repos, repo_scores)
        shipping_goal = _shipping_goal(top_repos)
        entries.append(
            MonthEntry(
                year=year,
                month=month,
                build_track=build_track,
                shipping_goal=shipping_goal,
            )
        )

    return entries


def render_block(entries: Sequence[MonthEntry], note: str) -> str:
    lines = [
        DEFAULT_HEADER,
        "",
        "| Month | Current Build Track | Shipping Goal |",
        "|---|---|---|",
    ]

    for entry in entries:
        month_label = datetime(entry.year, entry.month, 1).strftime("%b %Y")
        lines.append(
            f"| {month_label} | {entry.build_track} | {entry.shipping_goal} |"
        )

    lines.append("")
    lines.append(f"<sub> {note}</sub>")
    return "\n".join(lines)


def apply_readme_update(readme_text: str, block_markdown: str) -> tuple[str, bool]:
    managed_block = f"{START_MARKER}\n{block_markdown}\n{END_MARKER}"

    start_idx = readme_text.find(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        end_idx += len(END_MARKER)
        updated = readme_text[:start_idx] + managed_block + readme_text[end_idx:]
        return _normalize_spacing(updated), True

    insertion = "\n\n" + managed_block + "\n"
    updated = readme_text.rstrip() + insertion
    return _normalize_spacing(updated), False


def _normalize_spacing(text: str) -> str:
    return text.rstrip() + "\n"


def _recent_months(year: int, month: int, count: int) -> List[Tuple[int, int]]:
    pairs: List[Tuple[int, int]] = []
    y = year
    m = month
    for _ in range(count):
        pairs.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return pairs


def _build_track(top_repos: Sequence[Repo], repo_scores: Sequence[Tuple[Repo, int]]) -> str:
    if top_repos:
        if len(top_repos) == 1:
            return f"{top_repos[0].name} iteration cycle"
        return f"{top_repos[0].name} + {top_repos[1].name} iteration cycle"

    if repo_scores:
        return f"{repo_scores[0][0].name} maintenance cycle"

    return "Exploration and planning cycle"


def _shipping_goal(top_repos: Sequence[Repo]) -> str:
    keyword_bank = {
        "recomm": "Improve recommendation quality and UX clarity",
        "nlp": "Refine language pipelines and improve result relevance",
        "llm": "Harden LLM workflows and evaluation consistency",
        "ai": "Polish core AI workflows and docs for cleaner demos",
        "ml": "Consolidate experiments into reusable modules",
        "backend": "Strengthen API reliability and deployment readiness",
        "data": "Improve data quality checks and pipeline stability",
        "docs": "Tighten documentation for onboarding and demo readiness",
    }

    corpus_parts: List[str] = []
    for repo in top_repos:
        corpus_parts.extend(repo.topics)
        corpus_parts.append(repo.description)
        corpus_parts.append(repo.name)

    corpus = " ".join(corpus_parts).lower()
    for key, goal in keyword_bank.items():
        if key in corpus:
            return goal

    if top_repos:
        return "Ship cleaner milestones with better docs and reliability"

    return "Prepare next build track and align monthly shipping milestones"
