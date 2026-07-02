# CI_Spy_CD_Fly 🕵️✈️

A minimal Python library with a production-style CI/CD pipeline: automated linting, testing, coverage reporting, and deployment to GitHub Pages via GitHub Actions.

## Overview

`word_counter` is a small text-analysis library. The interesting part isn't the library — it's the pipeline around it: a two-stage GitHub Actions workflow that enforces code quality before anything is allowed to deploy.

```
push / PR ──▶ 🕵️ CI_Spy (lint → test → coverage)
                    │
                    ▼  gated on success, main branch only
              ✈️ CD_Fly (rebuild coverage report → deploy to GitHub Pages)
```

CD_Fly has a hard dependency on CI_Spy (`needs: ci_spy`). A failing lint check or a broken test makes deployment structurally impossible — not discouraged, not flagged, impossible.

## Tech Stack

| Component | Choice | Rationale |
|---|---|---|
| Language | Python 3.11 | Simple, fast to test and lint |
| CI/CD | GitHub Actions | Native to GitHub, no external service to configure |
| Testing | `pytest` + `pytest-cov` | Standard tooling, coverage reporting included |
| Linting | `flake8` | Fast, zero-config style enforcement |
| Deployment | GitHub Pages | Zero-secret deploy target, ideal for demonstrating the pattern |

## Pipeline Design

**`ci_spy`** — runs on every push and pull request:
1. Checkout + Python setup
2. Install package in editable mode + dev dependencies
3. Lint with `flake8`
4. Run `pytest` with coverage
5. Upload the HTML coverage report as a build artifact

**`cd_fly`** — runs only on push to `main`, only if `ci_spy` succeeds:
1. Rebuild the coverage report
2. Publish it to GitHub Pages via `actions/deploy-pages`

Restricting `cd_fly` to `push` (not `pull_request`) keeps deploys tied to a single source of truth — no accidental deploy from a fork or an unmerged branch.

## Results

- 6/6 tests passing, 100% line coverage on `src/word_counter`
- Full pipeline (lint → test → coverage → deploy) runs in under a minute on GitHub-hosted runners

## Design Decisions

- **`needs:` for hard gating** — `cd_fly` cannot execute unless `ci_spy` reports success. This is enforced by GitHub Actions itself, not by convention.
- **Branch + event restriction on deploy** — `if: github.ref == 'refs/heads/main' && github.event_name == 'push'` prevents PR runs from ever touching the deploy target.
- **`permissions:` scoped explicitly** — the workflow requests only `contents: read`, `pages: write`, `id-token: write`; nothing broader than what each job needs.
- **Coverage as a build artifact, not just a number** — the HTML report is both uploaded per-run and republished on deploy, so regressions are inspectable, not just a percentage in a log.

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/CI_Spy_CD_Fly.git
cd CI_Spy_CD_Fly
pip install -e .
pip install -r requirements-dev.txt
```

## Usage

```bash
flake8 src tests --max-line-length=100       # lint, mirrors ci_spy
pytest --cov=word_counter --cov-report=html  # test + coverage, mirrors ci_spy
```

```python
from word_counter import count_words, most_common_words, average_word_length

count_words("hello world")             # 2
most_common_words("cat dog cat", 1)    # [("cat", 2)]
average_word_length("cat dog")         # 3.0
```

## Roadmap

- **Matrix testing** across Python 3.9–3.12 to catch version-specific regressions
- **Dependency caching** via `actions/cache` to reduce CI runtime
- **Status badge** in this README, sourced from the workflow's live status
- **Pluggable deploy target** — swap GitHub Pages for a real server (Render, Fly.io) to demonstrate secrets management
