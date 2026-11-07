"""Простой парсер командной строки с раскрытием переменных."""

import os
import re
from dataclasses import dataclass, field


@dataclass
class ParsedCommand:
    """Результат разбора строки: имя команды и её аргументы."""

    name: str
    args: list[str] = field(default_factory=list)


def expand_vars(text: str) -> str:
    """Раскрыть переменные окружения в строке."""
    def replacer(match: re.Match) -> str:
        var_name = match.group(1) or match.group(2)
        return os.environ.get(var_name, match.group(0))

    pattern = re.compile(
        r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\$([a-zA-Z_][a-zA-Z0-9_]*)"
    )
    return pattern.sub(replacer, text)


def parse(line: str) -> ParsedCommand | None:
    """Разобрать строку ввода."""
    tokens = line.strip().split()
    if not tokens:
        return None
    expanded_tokens = [expand_vars(token) for token in tokens]
    return ParsedCommand(name=expanded_tokens[0], args=expanded_tokens[1:])
