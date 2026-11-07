"""Реестр всех команд эмулятора."""

from collections.abc import Callable

from .base import Command
from .cd import CdCommand
from .exit import ExitCommand
from .ls import LsCommand


# Фабрика: функция, которая возвращает экземпляр команды.
CommandFactory = Callable[[], Command]


_COMMAND_FACTORIES: dict[str, CommandFactory] = {
    "ls": lambda: LsCommand(),
    "cd": lambda: CdCommand(),
    "exit": lambda: ExitCommand(),
}


def get_command(name: str) -> Command | None:
    """Получить команду по имени.

    Args:
        name: имя команды.

    Returns:
        Экземпляр команды или None, если не найдена.
    """
    factory = _COMMAND_FACTORIES.get(name)
    if factory is None:
        return None
    return factory()
