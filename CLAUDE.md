# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PingPong is an app to support the PingPong College RCT study with:
- Backend: FastAPI (Python 3.11+), async SQLAlchemy, Pydantic v2, PyAirtable
- Frontend: SvelteKit with TypeScript
  - `web/study` (Svelte 5, Tailwind v4, bits-ui)
- Authorization: PyAirtable
- Authentication: JWT (magic links)

## Repo Layout

- `pingpong/` FastAPI app, models, schemas, authz, integrations
- `web/study/` study dashboard UI (Svelte 5)
- `scripts/` one-off scripts and CLI helpers
- `config.toml` configuration defaults

## Common Development Commands

### Backend (repo root)

```bash
uv sync
CONFIG_PATH=config.local.toml uv run fastapi dev pingpong --port 8000 --host 0.0.0.0 --reload
```

### Frontend: study dashboard (`web/study`)

```bash
pnpm install
pnpm dev
pnpm check
pnpm lint
pnpm format
```

### Docker

```bash
./start-dev-docker.sh
```

## Backend Architecture and Patterns

- Request middleware order: session parsing -> authz session -> DB session -> logging. Access `request.state.db`, `request.state.authz`, `request.state.session`.
- Authorization uses composable expressions in `pingpong/permission.py` (`Authz`, `LoggedIn`, `InstitutionAdmin`).
- Schemas live in `pingpong/schemas.py` (Pydantic v2). Return schemas directly from endpoints.
- Central config is `pingpong/config.py` via `BaseSettings` and TOML (`CONFIG_PATH=config.local.toml`).

## Frontend Architecture and Patterns

### `web/study` (Svelte 5)

- Svelte 5 runes and `.svelte.ts` modules appear throughout; follow those patterns.
- UI uses Tailwind v4, bits-ui, and components under `src/lib/components`/`src/lib/components/ui`.

## Code Style and Conventions

### Python
- Follow existing async-first patterns and type hints.
- Keep imports grouped: stdlib, third-party, local.
- Use logging via `logging.getLogger(__name__)` and raise `HTTPException` for HTTP errors.
- Prefer Pydantic models for request/response shapes instead of raw dicts.

### Svelte/TypeScript

`web/study`:
- Prettier uses tabs, single quotes, no trailing commas, print width 100.
- ESLint flat config; keep formatting consistent with existing files.

## Adding New API Endpoints

1. Add route handlers in `pingpong/server.py` alongside related endpoints.
2. Add/extend Pydantic schemas in `pingpong/schemas.py`.
3. Apply permission expressions via PyAirtable.
4. Implement client call in `web/study/src/lib/api.ts`.

## Development Notes

- Dev email uses the mock sender; check API console output for magic links.
