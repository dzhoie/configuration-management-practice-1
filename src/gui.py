"""Графический интерфейс эмулятора (GUI) на tkinter."""

import tkinter as tk
from tkinter import scrolledtext

from .commands import get_command
from .commands.exit import ExitRequested
from .errors import ShellError, UnknownCommandError
from .parser import parse
from .prompt import build_prompt


class EmulatorGUI:
    """Главное окно эмулятора."""

    def __init__(self) -> None:
        """Создать и настроить главное окно."""
        self.root = tk.Tk()
        self.root.title(f"Эмулятор - [{build_prompt().strip('$ ')}]")
        self.root.geometry("800x600")

        self.output_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Consolas", 11),
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        self.entry = tk.Entry(
            bottom_frame, font=("Consolas", 12), bg="#f0f0f0"
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.on_enter) 

        self.btn = tk.Button(
            bottom_frame,
            text="Выполнить",
            command=self.on_submit,
            font=("Arial", 10),
        )
        self.btn.pack(side=tk.RIGHT)

    
        self.write_line(f"Эмулятор запущен: {build_prompt().strip('$ ')}")
        self.write_line("VFS: не загружена")
        self.write_line("Стартовый скрипт: не задан")
        self.write_line("")
        self.entry.focus()

    def write_line(self, text: str = "") -> None:
        """Добавить строку в область вывода.

        Args:
            text: текст для вывода.
        """
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)

    def on_enter(self, event: tk.Event) -> None:
        """Обработчик нажатия Enter в поле ввода."""
        self.on_submit()

    def on_submit(self) -> None:
        """Обработчик нажатия кнопки или Enter.

        Берёт строку из поля ввода, выполняет и выводит результат.
        """
        line = self.entry.get().strip()
        if not line:
            return

        self.write_line(f"{build_prompt()}{line}")
        self.entry.delete(0, tk.END)

        parsed = parse(line)
        if parsed is None:
            return

        command = get_command(parsed.name)
        if command is None:
            self.write_line(f"Error: unknown command: '{parsed.name}'")
            return

        try:
            result = command.execute(parsed.args)
            if result:
                self.write_line(result)
        except ExitRequested:
            self.write_line("Bye!")
            self.root.after(500, self.root.destroy)
        except ShellError as exc:
            self.write_line(f"Error: {exc}")
        except Exception as exc: 
            self.write_line(f"Unexpected error: {exc}")

    def run(self) -> None:
        """Запустить главный цикл приложения."""
        self.root.mainloop()
