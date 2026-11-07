"""Графический интерфейс эмулятора (GUI)."""

import tkinter as tk
from tkinter import scrolledtext
from .config import Config
from .repl import Repl
from .prompt import build_prompt
from .startup import load_script


class EmulatorGUI:
    """Главное окно эмулятора."""

    def __init__(self, cfg: Config) -> None:
        """Создать и настроить главное окно."""
        self.cfg = cfg
        self.repl = Repl()
        
        self.root = tk.Tk()
        self.root.title(f"Эмулятор - [{build_prompt().strip('$ ')}]")
        self.root.geometry("800x600")

        self.output_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 11)
        )
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        self.entry = tk.Entry(bottom_frame, font=("Consolas", 12))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.on_enter)

        self.btn = tk.Button(
            bottom_frame, text="Выполнить", command=self.on_submit
        )
        self.btn.pack(side=tk.RIGHT)

        self.write_line(f"Эмулятор запущен: {build_prompt().strip('$ ')}")
        vfs_text = self.cfg.vfs_path if self.cfg.vfs_path else 'не загружена'
        self.write_line(f"VFS: {vfs_text}")
        scr_text = self.cfg.script_path if self.cfg.script_path else 'не задан'
        self.write_line(f"Стартовый скрипт: {scr_text}")
        self.write_line("-" * 40)

        if self.cfg.script_path:
            try:
                commands = load_script(self.cfg.script_path)
                for cmd in commands:
                    self.write_line(f"{build_prompt()}{cmd}")
                    res = self.repl.process_line(cmd)
                    if "Error" in res:
                        self.write_line(res)
                        self.write_line("[!] Скрипт остановлен из-за ошибки.")
                        break
                    if res:
                        self.write_line(res)
                self.write_line("-" * 40)
            except Exception as e:
                self.write_line(f"Ошибка скрипта: {e}")

        self.entry.focus()

    def write_line(self, text: str = "") -> None:
        """Добавить строку в область вывода."""
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, text + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)

    def on_enter(self, event: tk.Event) -> None:
        """Обработчик нажатия Enter в поле ввода."""
        self.on_submit()

    def on_submit(self) -> None:
        """Обработчик нажатия кнопки или Enter."""
        line = self.entry.get().strip()
        if not line: 
            return
        self.write_line(f"{build_prompt()}{line}")
        self.entry.delete(0, tk.END)
        res = self.repl.process_line(line)
        if res == "Bye!":
            self.write_line(res)
            self.root.after(500, self.root.destroy)
        elif res:
            self.write_line(res)

    def run(self) -> None:
        """Запустить главный цикл приложения."""
        self.root.mainloop()
