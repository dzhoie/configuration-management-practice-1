"""REPL — Read-Eval-Print Loop эмулятора."""

from .commands import get_command
from .commands.exit import ExitRequested
from .errors import ShellError, UnknownCommandError
from .parser import parse
from .prompt import build_prompt


class Repl:
    """Интерактивный цикл эмулятора оболочки."""

    def prompt(self) -> str:
        """Сформировать строку приглашения."""
        return build_prompt()

    def run(self) -> None:
        """Запустить цикл REPL до команды exit или Ctrl+D."""
        while True:
            try:
                line = input(self.prompt())
            except EOFError:
                print()
                break

            try:
                self.handle(line)
            except ExitRequested:
                print("Bye!")
                break
            except ShellError as exc:
                print(f"Error: {exc}")
            except Exception as exc:
                print(f"Unexpected error: {exc}")

    def handle(self, line: str) -> None:
        """Обработать одну строку ввода.

        Args:
            line: сырая строка от пользователя.

        Raises:
            ShellError: при ошибках выполнения команды.
            ExitRequested: при команде exit.
        """
        parsed = parse(line)
        if parsed is None:
            return

        command = get_command(parsed.name)
        if command is None:
            raise UnknownCommandError(parsed.name)

        result = command.execute(parsed.args)
        if result:
            print(result)
