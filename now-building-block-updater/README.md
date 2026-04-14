# Now Building Block Updater

Automatically inserts or updates a managed "Now Building" section in a README by analyzing monthly GitHub repository activity.

## What it does

- If the managed block does not exist, it inserts one.
- If the managed block exists, it updates it in-place.
- Generates month-wise rows with:
  - `Month`
  - `Current Build Track`
  - `Shipping Goal`
- Supports public repositories and private repositories that your token can access.

## Managed block markers

The updater manages content between these markers:

```md
<!-- NOW_BUILDING:START -->
... generated content ...
<!-- NOW_BUILDING:END -->
```

If markers are missing, the tool appends a new managed block to the end of the README.

## Install

From source:

```bash
python -m pip install -e .
```

From GitHub (after publishing this repository):

```bash
python -m pip install git+https://github.com/<owner>/now-building-block-updater.git
```

## Usage

```bash
now-building-updater \
  --username TridentifyIshaan \
  --readme-path README.md \
  --months 3 \
  --include-private
```

### Optional flags

- `--dry-run`: print generated managed block without writing files
- `--include-forks`: include forked repositories in scoring
- `--include-archived`: include archived repositories in scoring
- `--note`: footer note text under the table
- `--token-env`: env var name for token (default `GITHUB_TOKEN`)

## Private repository behavior

- Public repos are always analyzable.
- Private repos are included only if the token has access.
- Full private coverage for a user usually requires a token owned by that user.

## GitHub Actions setup

Use the workflow at [.github/workflows/monthly-update.yml](.github/workflows/monthly-update.yml).

Required repository variables:

- `NOW_BUILDING_USERNAME`: target GitHub username
- `NOW_BUILDING_README_PATH` (optional): defaults to `README.md`
- `NOW_BUILDING_MONTHS` (optional): defaults to `3`

Required repository secret:

- `NOW_BUILDING_TOKEN`: token with metadata read access and repository access needed for your scope

Token guidance:

- Public-only mode: default `GITHUB_TOKEN` may be enough.
- Private mode: use a fine-grained PAT in `NOW_BUILDING_TOKEN` with access to required private repositories.

## Reusable action usage

After publishing this repository, other projects can use it directly:

```yaml
name: Update Now Building

on:
  schedule:
    - cron: "5 1 1 * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: <owner>/now-building-block-updater@v1
        with:
          github-token: ${{ secrets.NOW_BUILDING_TOKEN }}
          username: TridentifyIshaan
          readme-path: README.md
          months: "3"
          include-private: "true"
      - name: Commit changes
        run: |
          if git diff --quiet; then
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git commit -m "chore: monthly now building update"
          git push
```

## Example generated block

```md
<!-- NOW_BUILDING:START -->
## Now Building

| Month | Current Build Track | Shipping Goal |
|---|---|---|
| Apr 2026 | RepoA + RepoB iteration cycle | Polish core AI workflows and docs for cleaner demos |
| Mar 2026 | RepoC iteration cycle | Improve recommendation quality and UX clarity |
| Feb 2026 | RepoD maintenance cycle | Consolidate experiments into reusable modules |

<sub> ♻️ Updating this block every month!.</sub>
<!-- NOW_BUILDING:END -->
```

## How to publish this as a separate reusable repository

1. Create a new repository, for example `now-building-block-updater`.
2. Copy this folder content to that new repository root.
3. Tag versions (`v0.1.0`, `v0.2.0`, ...).
4. Add release notes and usage examples.
5. Optionally publish to PyPI for `pip install` support.
