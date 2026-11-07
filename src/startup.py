"""Чтение и выполнение стартового скрипта."""

from pathlib import Path


class StartupError(Exception):
    """Ошибка чтения или выполнения стартового скрипта."""


def load_script(path: Path) -> list[str]:
    """Прочитать стартовый скрипт."""
    if not path.exists():
        raise StartupError(f"startup script not found: {path}")

    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        lines.append(line)
    return lines
