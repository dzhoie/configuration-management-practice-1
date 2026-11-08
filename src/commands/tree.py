"""Команда tree — вывод дерева каталогов."""


class TreeCommand:
    """Команда tree. Показывает дерево файлов и папок."""

    def __init__(self, vfs):
        """Создать команду с доступом к VFS."""
        self.vfs = vfs

    def execute(self, args):
        """Выполнить tree."""
        if not self.vfs:
            return "tree: VFS не загружена"

        path = args[0] if args else ""
        node = self.vfs.get_node(path)
        if not node:
            return f"tree: {path}: No such file or directory"
        return self.vfs.build_tree(node)
