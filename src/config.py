"""Разбор параметров командной строки."""

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


class ConfigError(Exception):
    """Ошибка чтения конфигурации."""


@dataclass
class Config:
    """Параметры запуска эмулятора."""

    vfs_path: Path | None = None
    script_path: Path | None = None


def parse_cli(argv: list[str] | None = None) -> Config:
    """Разобрать аргументы командной строки.

    Args:
        argv: список аргументов (по умолчанию — sys.argv[1:]).

    Returns:
        Config с заполненными полями из CLI.
    """
    parser = argparse.ArgumentParser(
        prog="shell-emulator",
        description="Эмулятор оболочки ОС. Вариант №6. Этап 2.",
    )
    parser.add_argument(
        "--vfs",
        type=Path,
        default=None,
        help="Путь к физическому расположению VFS.",
    )
    parser.add_argument(
        "--script",
        type=Path,
        default=None,
        help="Путь к стартовому скрипту.",
    )
    ns = parser.parse_args(argv)
    return Config(
        vfs_path=ns.vfs,
        script_path=ns.script,
    )


def debug_dump(cfg: Config) -> None:
    """Напечатать отладочный вывод параметров.

    Args:
        cfg: итоговый Config.
    """
    print("[DEBUG] Configuration", file=sys.stderr)
    print(f"[DEBUG]   vfs_path    = {cfg.vfs_path}", file=sys.stderr)
    print(f"[DEBUG]   script_path = {cfg.script_path}", file=sys.stderr)


def load(argv: list[str] | None = None) -> Config:
    """Загрузить конфигурацию.

    Порядок:
    1. Разобрать CLI.
    2. Показать отладочный вывод.

    Args:
        argv: аргументы (по умолчанию — sys.argv[1:]).

    Returns:
        Итоговый Config.
    """
    cfg = parse_cli(argv)
    debug_dump(cfg)
    return cfg
