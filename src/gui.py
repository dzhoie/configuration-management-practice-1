"""Графический интерфейс эмулятора (GUI)."""

import os
import tkinter as tk
from tkinter import scrolledtext
from .config import Config
from .repl import Repl
from .prompt import build_prompt
from .startup import load_script
from .vfs import VFS


class EmulatorGUI:
    """Главное окно эмулятора."""

    def __init__(self, cfg: Config) -> None:
        """Создать и настроить главное окно."""
        self.cfg = cfg

        vfs_path = (
            str(self.cfg.vfs_path)
            if self.cfg.vfs_path
            else "vfs_test/vfs.csv"
        )

        if not os.path.exists(vfs_path):
            base_dir = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
            alt_path = os.path.join(base_dir, vfs_path)
            if os.path.exists(alt_path):
                vfs_path = alt_path

        try:
            self.vfs = VFS(vfs_path)
            vfs_status = vfs_path
        except Exception as e:
            self.vfs = None
            vfs_status = f"Ошибка загрузки ({e})"

        self.repl = Repl(self.vfs)

        self.root = tk.Tk()
        self.root.title(f"Эмулятор - [{build_prompt().strip('$ ')}]")
        self.root.geometry("800x600")

        self.output_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state=tk.DISABLED,
            font=("Consolas", 11)
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
        self.write_line(f"VFS: {vfs_status}")
        scr_text = self.cfg.script_path if self.cfg.script_path else 'не задан'
        self.write_line(f"Стартовый скрипт: {scr_text}")
        self.write_line("-" * 40)

        if self.cfg.script_path:
            try:
                commands = load_script(self.cfg.script_path)
                for cmd in commands:
                    self.write_line(f"{build_prompt()}{cmd}")
                    res = self.repl.process_line(cmd)
                    if "Error" in res or res == "Bye!" or "cannot" in res:
                        if res:
                            self.write_line(res)
                        if res != "Bye!":
                            msg = "[!] Скрипт остановлен из-за ошибки."
                            self.write_line(msg)
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
