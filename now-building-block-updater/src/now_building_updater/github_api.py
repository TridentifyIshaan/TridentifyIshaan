from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional

import requests

API_BASE = "https://api.github.com"


@dataclass
class Repo:
    name: str
    full_name: str
    owner: str
    private: bool
    archived: bool
    fork: bool
    description: str
    topics: List[str]


class GitHubApiError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: Optional[str], timeout_seconds: int = 30) -> None:
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "now-building-block-updater/0.1.0",
            }
        )
        if token:
            self._session.headers["Authorization"] = f"Bearer {token}"
        self._timeout_seconds = timeout_seconds

    def get_authenticated_login(self) -> Optional[str]:
        response = self._session.get(f"{API_BASE}/user", timeout=self._timeout_seconds)
        if response.status_code == 401:
            return None
        if response.status_code >= 400:
            raise GitHubApiError(f"/user failed: {response.status_code} {response.text}")
        payload = response.json()
        return payload.get("login")

    def list_repos_for_user(self, username: str, include_private: bool) -> List[Repo]:
        repos: List[Repo] = []

        if include_private:
            auth_login = self.get_authenticated_login()
            if auth_login and auth_login.lower() == username.lower():
                repos.extend(self._list_authenticated_owned_repos())
            else:
                repos.extend(self._list_public_repos(username))
        else:
            repos.extend(self._list_public_repos(username))

        deduped: Dict[str, Repo] = {repo.full_name.lower(): repo for repo in repos}
        return list(deduped.values())

    def _list_authenticated_owned_repos(self) -> List[Repo]:
        repos: List[Repo] = []
        page = 1
        while True:
            response = self._session.get(
                f"{API_BASE}/user/repos",
                params={
                    "affiliation": "owner",
                    "per_page": 100,
                    "page": page,
                    "sort": "updated",
                    "direction": "desc",
                },
                timeout=self._timeout_seconds,
            )
            if response.status_code >= 400:
                raise GitHubApiError(
                    f"/user/repos failed: {response.status_code} {response.text}"
                )
            page_items = response.json()
            if not page_items:
                break
            repos.extend(self._to_repo(item) for item in page_items)
            page += 1
        return repos

    def _list_public_repos(self, username: str) -> List[Repo]:
        repos: List[Repo] = []
        page = 1
        while True:
            response = self._session.get(
                f"{API_BASE}/users/{username}/repos",
                params={
                    "type": "owner",
                    "per_page": 100,
                    "page": page,
                    "sort": "updated",
                    "direction": "desc",
                },
                timeout=self._timeout_seconds,
            )
            if response.status_code >= 400:
                raise GitHubApiError(
                    f"/users/{username}/repos failed: {response.status_code} {response.text}"
                )
            page_items = response.json()
            if not page_items:
                break
            repos.extend(self._to_repo(item) for item in page_items)
            page += 1
        return repos

    def _to_repo(self, payload: dict) -> Repo:
        return Repo(
            name=payload.get("name", ""),
            full_name=payload.get("full_name", ""),
            owner=(payload.get("owner") or {}).get("login", ""),
            private=bool(payload.get("private", False)),
            archived=bool(payload.get("archived", False)),
            fork=bool(payload.get("fork", False)),
            description=payload.get("description") or "",
            topics=payload.get("topics") or [],
        )

    def count_commits(
        self,
        owner: str,
        repo: str,
        since_iso: str,
        until_iso: str,
    ) -> int:
        response = self._session.get(
            f"{API_BASE}/repos/{owner}/{repo}/commits",
            params={"since": since_iso, "until": until_iso, "per_page": 1},
            timeout=self._timeout_seconds,
        )
        if response.status_code == 409:
            return 0
        if response.status_code == 422:
            return 0
        if response.status_code >= 400:
            raise GitHubApiError(
                f"/repos/{owner}/{repo}/commits failed: {response.status_code} {response.text}"
            )

        data = response.json()
        if not data:
            return 0

        link_header = response.headers.get("Link", "")
        if link_header:
            last_page = _parse_last_page(link_header)
            if last_page:
                return last_page

        return len(data)


def _parse_last_page(link_header: str) -> Optional[int]:
    for part in link_header.split(","):
        if 'rel="last"' not in part:
            continue
        section = part.split(";")[0].strip()
        if not section.startswith("<") or not section.endswith(">"):
            continue
        url = section[1:-1]
        marker = "page="
        idx = url.rfind(marker)
        if idx == -1:
            continue
        page_value = []
        for char in url[idx + len(marker) :]:
            if char.isdigit():
                page_value.append(char)
            else:
                break
        if page_value:
            return int("".join(page_value))
    return None


def iso_month_range(year: int, month: int) -> tuple[str, str]:
    start = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    else:
        end = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    return start.isoformat().replace("+00:00", "Z"), end.isoformat().replace("+00:00", "Z")


def parse_github_reset_time(reset_header: Optional[str]) -> Optional[datetime]:
    if not reset_header:
        return None

    try:
        reset_epoch = int(reset_header)
        return datetime.fromtimestamp(reset_epoch, tz=timezone.utc)
    except ValueError:
        pass

    try:
        parsed = parsedate_to_datetime(reset_header)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None
