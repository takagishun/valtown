from __future__ import annotations

import sqlite3
from pathlib import Path

from migrate import migrate

DEFAULT_DB_PATH = Path(".tmp/app.sqlite3")


def reset_db(db_path: str | Path = DEFAULT_DB_PATH) -> None:
    db_path = Path(db_path)
    db_path.unlink(missing_ok=True)
    migrate(db_path)
    seed(db_path)


def seed(db_path: str | Path) -> None:
    with sqlite3.connect(db_path) as conn:
        columns = {
            row[1]
            for row in conn.execute("pragma table_info(vals)").fetchall()
        }
        owner_column = "username" if "username" in columns else "handle"
        conn.execute(
            f"insert into vals (id, {owner_column}, code) values (?, ?, ?)",
            (1, "sophie", "export const hello = 'world';"),
        )


if __name__ == "__main__":
    reset_db()
    print(f"reset {DEFAULT_DB_PATH}")
