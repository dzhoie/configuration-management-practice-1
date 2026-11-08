"""Реестр всех команд эмулятора."""

from .ls import LsCommand
from .cd import CdCommand
from .exit import ExitCommand
from .pwd import PwdCommand
from .tree import TreeCommand
from .rmdir import RmdirCommand
from .help import HelpCommand


def get_command(name: str, vfs):
    """Получить команду по имени."""
    commands = {
        "ls": LsCommand(vfs),
        "cd": CdCommand(vfs),
        "exit": ExitCommand(),
        "pwd": PwdCommand(vfs),
        "tree": TreeCommand(vfs),
        "rmdir": RmdirCommand(vfs),
        "help": HelpCommand(),
    }
    return commands.get(name)
