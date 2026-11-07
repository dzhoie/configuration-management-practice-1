"""Формирование приглашения к вводу на основе данных ОС."""

import getpass
import socket
from pathlib import Path


def get_username() -> str:
    """Получить имя текущего пользователя."""
    try:
        return getpass.getuser()
    except Exception:
        return "unknown"


def get_hostname() -> str:
    """Получить имя хоста (компьютера)."""
    try:
        return socket.gethostname()
    except Exception:
        return "localhost"


def get_short_cwd() -> str:
    """Получить сокращённый путь текущей директории."""
    try:
        cwd = Path.cwd()
        home = Path.home()
        if cwd == home:
            return "~"
        if cwd.is_relative_to(home):
            rel = cwd.relative_to(home)
            return f"~/{rel}"
        return str(cwd)
    except Exception:
        return "?"


def build_prompt() -> str:
    """Сформировать приглашение к вводу (username@host:cwd$)."""
    user = get_username()
    host = get_hostname()
    cwd = get_short_cwd()
    return f"{user}@{host}:{cwd}$ "
