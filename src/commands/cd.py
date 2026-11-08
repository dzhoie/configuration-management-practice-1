"""Команда cd — смена текущей директории."""


class CdCommand:
    """Команда cd. Меняет текущую директорию в VFS."""

    def __init__(self, vfs):
        """Создать команду с доступом к VFS."""
        self.vfs = vfs

    def execute(self, args):
        """Выполнить cd."""
        if not args:
            return ""
        try:
            self.vfs.change_dir(args[0])
            return ""
        except Exception:
            return f"cd: {args[0]}: No such file or directory"
