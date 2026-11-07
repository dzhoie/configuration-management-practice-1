"""Тесты стартового скрипта."""

from pathlib import Path

import pytest

from src.startup import StartupError, load_script


def test_load_script_simple(tmp_path: Path) -> None:
    """Простой скрипт без комментариев."""
    script = tmp_path / "start.txt"
    script.write_text("ls\ncd /home\n", encoding="utf-8")
    commands = load_script(script)
    assert commands == ["ls", "cd /home"]


def test_load_script_full_line_comments(tmp_path: Path) -> None:
    """Полные строки-комментарии игнорируются."""
    script = tmp_path / "start.txt"
    script.write_text(
        "# Комментарий\nls\n# Ещё комментарий\ncd /home\n",
        encoding="utf-8",
    )
    commands = load_script(script)
    assert commands == ["ls", "cd /home"]


def test_load_script_inline_comments(tmp_path: Path) -> None:
    """Inline-комментарии после команды игнорируются."""
    script = tmp_path / "start.txt"
    script.write_text(
        "ls  # список файлов\ncd /home  # переход\n",
        encoding="utf-8",
    )
    commands = load_script(script)
    assert commands == ["ls", "cd /home"]


def test_load_script_empty_lines(tmp_path: Path) -> None:
    """Пустые строки игнорируются."""
    script = tmp_path / "start.txt"
    script.write_text("\n\nls\n\n\ncd\n\n", encoding="utf-8")
    commands = load_script(script)
    assert commands == ["ls", "cd"]


def test_load_script_missing() -> None:
    """Несуществующий файл — StartupError."""
    with pytest.raises(StartupError):
        load_script(Path("/nonexistent/start.txt"))


def test_load_script_empty(tmp_path: Path) -> None:
    """Пустой скрипт — пустой список."""
    script = tmp_path / "start.txt"
    script.write_text("", encoding="utf-8")
    assert load_script(script) == []


def test_load_script_only_comments(tmp_path: Path) -> None:
    """Скрипт только из комментариев — пустой список."""
    script = tmp_path / "start.txt"
    script.write_text("# один\n# два\n", encoding="utf-8")
    assert load_script(script) == []
