from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Dict, List, Sequence, Tuple

from .github_api import GitHubClient, Repo, iso_month_range

START_MARKER = "<!-- NOW_BUILDING:START -->"
END_MARKER = "<!-- NOW_BUILDING:END -->"
DEFAULT_HEADER = "## Now Building"
NOISE_NAME_PARTS = (
    "readme",
    "profile",
    "dotfiles",
    "template",
    "updater",
    "config",
)


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
    rows_per_month: int,
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
    used_goals: set[str] = set()
    row_count = max(1, rows_per_month)
    for index, (year, month) in enumerate(month_pairs):
        since_iso, until_iso = iso_month_range(year, month)
        repo_scores: List[Tuple[Repo, int]] = []

        for repo in repos:
            if _is_noise_repo(repo, username):
                continue
            commits = github.count_commits(repo.owner, repo.name, since_iso, until_iso)
            if commits <= 0:
                continue
            repo_scores.append((repo, commits))

        repo_scores.sort(key=lambda item: item[1], reverse=True)

        if not repo_scores:
            build_track = _build_track([], repo_scores, index, 0)
            shipping_goal = _shipping_goal([], index, 0, used_goals)
            used_goals.add(shipping_goal)
            entries.append(
                MonthEntry(
                    year=year,
                    month=month,
                    build_track=build_track,
                    shipping_goal=shipping_goal,
                )
            )
            continue

        month_repo_scores = repo_scores[:row_count]
        for row_index, (repo, _commit_count) in enumerate(month_repo_scores):
            top_repos = [repo]
            build_track = _build_track(top_repos, repo_scores, index, row_index)
            shipping_goal = _shipping_goal(top_repos, index, row_index, used_goals)
            used_goals.add(shipping_goal)
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

    previous_label = ""
    for entry in entries:
        month_label = datetime(entry.year, entry.month, 1).strftime("%b %Y")
        visible_month = month_label if month_label != previous_label else ""
        lines.append(
            f"| {visible_month} | {entry.build_track} | {entry.shipping_goal} |"
        )
        previous_label = month_label

    lines.append("")
    lines.append(f"<sub> {note}</sub>")
    return "\n".join(lines)


def apply_readme_update(readme_text: str, block_markdown: str) -> tuple[str, bool]:
    managed_block = f"{START_MARKER}\n{block_markdown}\n{END_MARKER}"

    start_idx = readme_text.find(START_MARKER)
    end_idx = readme_text.find(END_MARKER)

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        end_idx += len(END_MARKER)
        updated = _splice_managed_block(
            prefix=readme_text[:start_idx],
            managed_block=managed_block,
            suffix=readme_text[end_idx:],
        )
        return _normalize_spacing(updated), True

    legacy_range = _find_legacy_now_building_range(readme_text)
    if legacy_range is not None:
        legacy_start, legacy_end = legacy_range
        updated = _splice_managed_block(
            prefix=readme_text[:legacy_start],
            managed_block=managed_block,
            suffix=readme_text[legacy_end:],
        )
        return _normalize_spacing(updated), True

    insertion = "\n\n" + managed_block + "\n"
    updated = readme_text.rstrip() + insertion
    return _normalize_spacing(updated), False


def _find_legacy_now_building_range(readme_text: str) -> Tuple[int, int] | None:
    # Prefer replacing a complete legacy block that ends at the footer <sub> line.
    full_block_pattern = re.compile(
        r"(?ms)^##\s+Now\s+Building\s*\n.*?^<sub>.*?</sub>\s*\n?"
    )
    full_match = full_block_pattern.search(readme_text)
    if full_match:
        return full_match.start(), full_match.end()

    # Fallback: replace from heading until the next section heading.
    heading_pattern = re.compile(r"(?m)^##\s+Now\s+Building\s*$")
    heading_match = heading_pattern.search(readme_text)
    if not heading_match:
        return None

    next_heading_pattern = re.compile(r"(?m)^##\s+")
    next_match = next_heading_pattern.search(readme_text, heading_match.end())
    if next_match:
        return heading_match.start(), next_match.start()

    return heading_match.start(), len(readme_text)


def _normalize_spacing(text: str) -> str:
    return text.rstrip() + "\n"


def _splice_managed_block(prefix: str, managed_block: str, suffix: str) -> str:
    result = prefix + managed_block
    if suffix and not suffix.startswith("\n"):
        result += "\n"
    result += suffix
    return result


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


def _build_track(
    top_repos: Sequence[Repo],
    repo_scores: Sequence[Tuple[Repo, int]],
    month_index: int,
    row_index: int,
) -> str:
    if top_repos:
        repo = top_repos[0]
        theme = _detect_repo_theme(repo)
        theme_track_phrases = {
            "recommender": [
                "recommendation ranking refinement",
                "personalization signal tuning",
                "candidate retrieval improvements",
            ],
            "nlp": [
                "text pipeline quality upgrades",
                "prompt and parsing flow refinement",
                "language workflow stabilization",
            ],
            "llm": [
                "LLM workflow hardening",
                "retrieval and grounding improvements",
                "evaluation and guardrail upgrades",
            ],
            "data": [
                "data pipeline reliability work",
                "data quality and validation upgrades",
                "dataset curation and preprocessing improvements",
            ],
            "backend": [
                "API reliability and service cleanup",
                "backend stability and integration work",
                "service performance and error-handling upgrades",
            ],
            "mobile": [
                "mobile experience and flow polish",
                "feature integration and UI responsiveness tuning",
                "release-readiness cleanup for app workflows",
            ],
            "dsa": [
                "problem-solving pattern expansion",
                "algorithm implementation consistency work",
                "DSA practice structure and coverage upgrades",
            ],
            "ml": [
                "model experimentation and iteration",
                "feature engineering and evaluation improvements",
                "training pipeline stabilization",
            ],
            "general": [
                "core feature development",
                "integration and stability improvements",
                "delivery-focused polish work",
            ],
        }
        phrase = _pick_by_offset(
            theme_track_phrases.get(theme, theme_track_phrases["general"]),
            month_index + row_index,
        )
        return f"{repo.name}: {phrase}"

    if repo_scores:
        return f"{repo_scores[0][0].name}: maintenance and cleanup"

    return "Planning, exploration, and backlog shaping"


def _shipping_goal(
    top_repos: Sequence[Repo],
    month_index: int,
    row_index: int,
    used_goals: set[str],
) -> str:
    if top_repos:
        repo = top_repos[0]
        theme = _detect_repo_theme(repo)
        theme_goals = {
            "recommender": [
                "Lift recommendation relevance and reduce noisy suggestions",
                "Improve ranking quality with clearer user-intent signals",
                "Ship a more consistent personalization experience end to end",
            ],
            "nlp": [
                "Improve response relevance and text quality across key flows",
                "Reduce parsing and prompt edge cases in production paths",
                "Raise language workflow reliability for cleaner outputs",
            ],
            "llm": [
                "Reduce hallucination risk with stronger grounding and checks",
                "Stabilize evaluation metrics and model behavior across prompts",
                "Ship safer LLM features with clearer guardrails",
            ],
            "data": [
                "Reduce data breakages with stronger validation and monitoring",
                "Improve pipeline consistency from ingestion to model input",
                "Harden dataset quality checks for repeatable experiments",
            ],
            "backend": [
                "Improve API stability and reduce avoidable failure paths",
                "Lower latency and improve service reliability under load",
                "Tighten error handling and deployment readiness",
            ],
            "mobile": [
                "Polish app UX and reduce friction in core journeys",
                "Improve release readiness with better app stability",
                "Smoothen mobile feature flows for clearer user outcomes",
            ],
            "dsa": [
                "Increase consistency and depth across core DSA patterns",
                "Improve problem-solving speed through structured practice",
                "Strengthen implementation accuracy on medium-hard sets",
            ],
            "ml": [
                "Improve model quality with cleaner evaluation and iteration loops",
                "Convert experiments into reusable training components",
                "Stabilize model workflows for repeatable monthly progress",
            ],
            "general": [
                "Ship cleaner milestones with stronger reliability",
                "Close the month with production-ready demos and clearer docs",
                "Improve release readiness by tightening tests and workflows",
            ],
        }
        candidates = theme_goals.get(theme, theme_goals["general"])
    else:
        candidates = [
            "Prepare next build track and align monthly shipping milestones",
            "Finalize roadmap priorities and reduce execution blockers",
        ]

    rotated = _rotate(candidates, month_index + row_index)
    for candidate in rotated:
        if candidate not in used_goals:
            return candidate

    return rotated[0]


def _rotate(values: Sequence[str], offset: int) -> List[str]:
    if not values:
        return []
    shift = offset % len(values)
    return list(values[shift:]) + list(values[:shift])


def _is_noise_repo(repo: Repo, username: str) -> bool:
    name = repo.name.lower()
    if name == username.lower():
        return True
    return any(part in name for part in NOISE_NAME_PARTS)


def _detect_repo_theme(repo: Repo) -> str:
    corpus = _repo_corpus(repo)

    if any(token in corpus for token in ["recommend", "recsys", "recommender", "ranking"]):
        return "recommender"
    if any(token in corpus for token in ["llm", "rag", "prompt", "agent", "langchain"]):
        return "llm"
    if any(token in corpus for token in ["nlp", "text", "sentiment", "transformer", "language"]):
        return "nlp"
    if any(token in corpus for token in ["data", "etl", "pipeline", "analytics", "warehouse"]):
        return "data"
    if any(token in corpus for token in ["api", "backend", "server", "fastapi", "flask", "express"]):
        return "backend"
    if any(token in corpus for token in ["flutter", "android", "ios", "mobile", "dart"]):
        return "mobile"
    if any(token in corpus for token in ["dsa", "leetcode", "algorithm", "java", "cp"]):
        return "dsa"
    if any(token in corpus for token in ["ml", "model", "ai", "tensorflow", "sklearn", "keras"]):
        return "ml"

    return "general"


def _repo_corpus(repo: Repo) -> str:
    parts = [repo.name, repo.description, *repo.topics]
    return " ".join(parts).lower()


def _pick_by_offset(values: Sequence[str], offset: int) -> str:
    if not values:
        return "core feature development"
    return values[offset % len(values)]
