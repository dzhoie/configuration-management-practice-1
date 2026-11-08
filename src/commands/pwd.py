"""Команда pwd — вывод текущего пути."""


class PwdCommand:
    """Команда pwd. Показывает текущий путь в VFS."""

    def __init__(self, vfs):
        """Создать команду с доступом к VFS."""
        self.vfs = vfs

    def execute(self, args):
        """Выполнить pwd."""
        if not self.vfs:
            return "pwd: VFS не загружена"
        return self.vfs.get_pwd()
