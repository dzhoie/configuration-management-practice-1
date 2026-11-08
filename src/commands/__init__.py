"""Реестр всех команд эмулятора."""

from .ls import LsCommand
from .cd import CdCommand
from .exit import ExitCommand


def get_command(name: str, vfs):
    """Получить команду по имени."""
    commands = {
        "ls": LsCommand(vfs),
        "cd": CdCommand(vfs),
        "exit": ExitCommand(),
    }
    return commands.get(name)
