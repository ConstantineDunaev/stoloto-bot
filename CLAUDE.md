# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A Telegram bot (aiogram 3) that tracks Stoloto "4x20" lottery draws, stores draw history and winning
combinations in SQLite, and will eventually let users check a combination against historical draw
statistics. Text and bot replies are in Russian.

## Commands

This project uses `uv` for dependency management (Python >=3.13).

```
uv sync                          # install dependencies from uv.lock
uv run python -m src.main        # run the Telegram bot
uv run python dev.py             # one-off script: fetch page 1 of draws and write to DB
uv run python -m src.workers.fill_draws           # backfill/update draws from Stoloto archive (also runnable standalone)
uv run python -m src.workers.pull_unique_combination  # (re)generate the unique_combination lookup table
```

There are no tests or linter configs in this repo currently.

### Environment

Configuration is loaded from a `.env` file (see `src/config/__init__.py` for the full list of variables):
`DATABASE_PATH`, `GOSLOTO_PARTHNER` (Stoloto API partner header), `STOLOTO_GAME_NAME`,
`STOLOTO_DRAWS_FIRST_PAGE`/`STOLOTO_DRAWS_LAST_PAGE`/`STOLOTO_COUNT_DRAWS_ON_PAGE`/`STOLOTO_DELAY`/
`STOLOTO_DRAWS_UPDATE_INTERVAL`, `TELEGRAM_TOKEN`, `TELEGRAM_USERS` (comma-separated allow-list of user
IDs), `TELEGRAM_PROXY`.

## Architecture

- `src/stoloto/stoloto.py` — thin sync HTTP client (`Stoloto` class) for the Stoloto mobile archive API
  (`GET /p/api/mobile/api/v35/service/draws/archive`). Returns parsed `Draw` objects.
- `src/schemas/__init__.py` — Pydantic models. `Draw` maps the API's camelCase fields (`id`,
  `superPrize`, `winningCombination`) to snake_case and exposes `as_tuple()` (for the `draw` table row)
  and `combinations()` (expands the winning numbers into `(draw_id, position, value)` rows for the
  `combination` table).
- `src/database/__init__.py` — a single `Database` class wrapping raw `aiosqlite` SQL (no ORM). Owns
  `init()` (idempotent `CREATE TABLE IF NOT EXISTS`) and read/write methods. A new `Database(...)`
  instance is constructed per call site/worker — it's a thin stateless wrapper around a DB path, not a
  shared connection pool.
- Three tables: `draw` (one row per draw, `draw_id` PK, raw combination JSON kept too), `combination`
  (one row per draw per number position — used for statistics queries), `unique_combination` (lookup
  table of all possible N-number combinations from 1..20, generated offline by
  `src/utils/generate_combination`, used to compute combination rarity/stats — not yet wired into the bot).
- `src/workers/fill_draws.py` — polls the Stoloto archive page by page (bounded by
  `STOLOTO_DRAWS_FIRST_PAGE..STOLOTO_DRAWS_LAST_PAGE`), stops as soon as it hits a draw ID `<=` the max
  ID already stored, and sleeps `STOLOTO_DELAY` seconds between pages to avoid rate-limiting. Retries
  HTTP errors with linear backoff (`STOLOTO_DELAY * attempt`, 5 attempts). This is scheduled by
  `src/main.py` via APScheduler (`AsyncIOScheduler`, interval = `STOLOTO_DRAWS_UPDATE_INTERVAL`,
  `max_instances=1`) running in the same event loop as the bot.
- `src/bot/` — aiogram app:
  - `src/bot/__init__.py`: `start_bot()` starts the scheduler then `Dispatcher.start_polling`.
  - `src/bot/handlers/`: one router module per feature (`start`, `draws`, `check`), composed into
    `main_router` in `handlers/__init__.py`. `check.py`'s combination-lookup handler is currently
    commented out / unfinished — the stats query it depends on isn't implemented yet.
  - `src/bot/filters/user.py`: `UserFilter` — every handler is gated on `event_from_user.id` being in
    `Config.telegram_users`, i.e. this bot is a private allow-list bot, not public.
  - `src/bot/keyboards/reply/`: static `ReplyKeyboardMarkup` builders (currently just the "📊 Тиражи" button).
  - `src/bot/states/`: an `OperationState` FSM group exists but is not currently referenced by any handler.
- `database.sqlite3` at the repo root is the actual runtime DB (gitignored); `DATABASE_PATH` in `.env`
  points to it.
