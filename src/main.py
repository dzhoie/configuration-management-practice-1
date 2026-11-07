"""Точка входа в эмулятор оболочки (GUI)."""

import sys

from .gui import EmulatorGUI


def main() -> int:
    """Запустить эмулятор с графическим интерфейсом.

    Returns:
        Код возврата (0 — успех).
    """
    app = EmulatorGUI()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
