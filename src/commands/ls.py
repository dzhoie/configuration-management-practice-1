"""Команда ls — вывод содержимого директории."""


class LsCommand:
    """Команда ls. Выводит содержимое директории в VFS."""

    def __init__(self, vfs):
        """Создать команду с доступом к VFS."""
        self.vfs = vfs

    def execute(self, args):
        """Выполнить ls."""
        path = args[0] if args else ""
        try:
            items = self.vfs.list_dir(path)
            return "  ".join(items)
        except Exception:
            return "ls: cannot access: No such file or directory"
