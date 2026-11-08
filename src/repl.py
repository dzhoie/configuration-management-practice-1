"""REPL — Read-Eval-Print Loop эмулятора."""

from .commands import get_command
from .commands.exit import ExitRequested
from .errors import ShellError
from .parser import parse
from .prompt import build_prompt


class Repl:
    """Интерактивный цикл эмулятора оболочки."""

    def __init__(self, vfs=None):
        """Создать REPL с заданной VFS."""
        self.vfs = vfs

    def prompt(self) -> str:
        """Сформировать строку приглашения."""
        return build_prompt()

    def process_line(self, line: str) -> str:
        """Обработать строку без прерывания на ошибках."""
        parsed = parse(line)
        if parsed is None:
            return ""
        command = get_command(parsed.name, self.vfs)
        if command is None:
            return f"Error: unknown command: '{parsed.name}'"
        try:
            result = command.execute(parsed.args)
            return result if result else ""
        except ExitRequested:
            return "Bye!"
        except ShellError as exc:
            return f"Error: {exc}"
        except Exception as exc:
            return f"Unexpected error: {exc}"
