"""Команда rmdir — удаление пустой папки."""


class RmdirCommand:
    """Команда rmdir. Удаляет пустую папку в VFS."""

    def __init__(self, vfs):
        """Создать команду с доступом к VFS."""
        self.vfs = vfs

    def execute(self, args):
        """Выполнить rmdir."""
        if not self.vfs:
            return "rmdir: VFS не загружена"
        if not args:
            return "rmdir: missing operand"
        try:
            self.vfs.rmdir(args[0])
            return ""
        except Exception as e:
            return f"rmdir: failed to remove '{args[0]}': {e}"
