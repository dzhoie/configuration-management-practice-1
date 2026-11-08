"""Виртуальная файловая система (VFS) на основе CSV."""

import csv
import os


class VFSNode:
    """Узел файловой системы (папка или файл)."""

    def __init__(self, name, is_dir, content=""):
        """Инициализация узла."""
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {}


class VFS:
    """Виртуальная файловая система в памяти."""

    def __init__(self, csv_path):
        """Создать VFS и загрузить данные из CSV."""
        self.root = VFSNode("/", is_dir=True)
        self.cwd = self.root
        self._load_from_csv(csv_path)

    def _load_from_csv(self, csv_path):
        """Читает CSV и строит дерево в памяти."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Файл VFS не найден: {csv_path}")

        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                path = row["path"].strip()
                is_dir = row["type"].strip() == "dir"
                content = row.get("content", "")

                if path == "/":
                    continue

                parts = [p for p in path.split("/") if p]
                current = self.root
                for i, part in enumerate(parts):
                    is_last = (i == len(parts) - 1)
                    if part not in current.children:
                        current.children[part] = VFSNode(
                            part, is_dir if is_last else True
                        )

                    if not is_last:
                        current = current.children[part]
                    else:
                        if is_dir:
                            current.children[part].is_dir = True
                        else:
                            current.children[part].is_dir = False
                            current.children[part].content = content

    def get_node(self, path):
        """Найти узел по пути (абсолютному или относительному)."""
        if not path or path == ".":
            return self.cwd

        if path.startswith("/"):
            parts = [p for p in path.split("/") if p]
            current = self.root
        else:
            parts = [p for p in path.split("/") if p]
            current = self.cwd

        for part in parts:
            if part == "..":
                parent = self._find_parent(self.root, current)
                if parent:
                    current = parent
            elif part != ".":
                if part in current.children:
                    current = current.children[part]
                else:
                    return None
        return current

    def _find_parent(self, start_node, target_node):
        """Найти родителя."""
        if start_node == target_node:
            return None
        for child in start_node.children.values():
            if child == target_node:
                return start_node
            parent = self._find_parent(child, target_node)
            if parent:
                return parent
        return None

    def list_dir(self, path=""):
        """Вернуть список файлов в папке."""
        node = self.get_node(path)
        if not node or not node.is_dir:
            raise ValueError("Not a directory")
        return sorted(list(node.children.keys()))

    def change_dir(self, path):
        """Сменить текущую директорию."""
        node = self.get_node(path)
        if not node or not node.is_dir:
            raise ValueError("No such directory")
        self.cwd = node

    def get_pwd(self):
        """Получить текущий путь (для команды pwd)."""
        if self.cwd == self.root:
            return "/"
        parts = []
        node = self.cwd
        while node and node != self.root:
            parts.append(node.name)
            node = self._find_parent(self.root, node)
        return "/" + "/".join(reversed(parts))

    def build_tree(self, node=None, prefix="", is_last=True):
        """Рекурсивно строит строку для команды tree."""
        if node is None:
            node = self.root
            result = f"{node.name}\n"
        else:
            connector = "└── " if is_last else "├── "
            result = prefix + connector + node.name + "\n"
            prefix += "    " if is_last else "│   "

        children = sorted(list(node.children.values()), key=lambda x: x.name)
        for i, child in enumerate(children):
            is_last_child = (i == len(children) - 1)
            result += self.build_tree(child, prefix, is_last_child)
        return result

    def rmdir(self, path):
        """Удалить пустую папку из памяти."""
        node = self.get_node(path)
        if not node:
            raise ValueError("No such directory")
        if not node.is_dir:
            raise ValueError("Not a directory")
        if node.children:
            raise ValueError("Directory not empty")
        if node == self.root:
            raise ValueError("Cannot remove root")

        parent = self._find_parent(self.root, node)
        if parent:
            del parent.children[node.name]
