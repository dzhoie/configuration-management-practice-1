"""Реестр всех команд эмулятора."""

from .ls import LsCommand
from .cd import CdCommand
from .exit import ExitCommand
from .pwd import PwdCommand
from .tree import TreeCommand


def get_command(name: str, vfs):
    """Получить команду по имени."""
    commands = {
        "ls": LsCommand(vfs),
        "cd": CdCommand(vfs),
        "exit": ExitCommand(),
        "pwd": PwdCommand(vfs),
        "tree": TreeCommand(vfs),
    }
    return commands.get(name)
