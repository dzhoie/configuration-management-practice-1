"""Точка входа в эмулятор оболочки (GUI)."""

import sys
from .config import load
from .gui import EmulatorGUI


def main() -> int:
    """Запустить эмулятор с графическим интерфейсом."""
    cfg = load()
    app = EmulatorGUI(cfg)
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
