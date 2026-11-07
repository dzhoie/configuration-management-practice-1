"""Тесты конфигурации CLI."""

from pathlib import Path

from src.config import Config, parse_cli


def test_parse_cli_empty() -> None:
    """Пустой CLI даёт Config с None-полями."""
    cfg = parse_cli([])
    assert cfg.vfs_path is None
    assert cfg.script_path is None


def test_parse_cli_vfs_only(tmp_path: Path) -> None:
    """Только --vfs."""
    vfs = tmp_path / "vfs"
    cfg = parse_cli(["--vfs", str(vfs)])
    assert cfg.vfs_path == vfs
    assert cfg.script_path is None


def test_parse_cli_script_only(tmp_path: Path) -> None:
    """Только --script."""
    script = tmp_path / "start.txt"
    cfg = parse_cli(["--script", str(script)])
    assert cfg.vfs_path is None
    assert cfg.script_path == script


def test_parse_cli_both(tmp_path: Path) -> None:
    """Оба параметра."""
    vfs = tmp_path / "vfs"
    script = tmp_path / "start.txt"
    cfg = parse_cli(["--vfs", str(vfs), "--script", str(script)])
    assert cfg.vfs_path == vfs
    assert cfg.script_path == script


def test_config_dataclass() -> None:
    """Config можно создать напрямую."""
    cfg = Config(vfs_path=Path("a"), script_path=Path("b"))
    assert cfg.vfs_path == Path("a")
    assert cfg.script_path == Path("b")
