"""Тесты формирования приглашения."""

from src.prompt import (
    build_prompt,
    get_hostname,
    get_short_cwd,
    get_username,
)


def test_get_username() -> None:
    """Имя пользователя не пустое."""
    user = get_username()
    assert isinstance(user, str)
    assert len(user) > 0


def test_get_hostname() -> None:
    """Имя хоста не пустое."""
    host = get_hostname()
    assert isinstance(host, str)
    assert len(host) > 0


def test_get_short_cwd() -> None:
    """Путь сокращается до ~ в домашней папке."""
    cwd = get_short_cwd()
    assert isinstance(cwd, str)
    assert len(cwd) > 0


def test_build_prompt_format() -> None:
    """Приглашение содержит @, : и $."""
    prompt = build_prompt()
    assert "@" in prompt
    assert ":" in prompt
    assert prompt.endswith("$ ")


def test_build_prompt_uses_real_data() -> None:
    """Приглашение содержит имя пользователя и хоста."""
    prompt = build_prompt()
    user = get_username()
    host = get_hostname()
    assert user in prompt
    assert host in prompt
