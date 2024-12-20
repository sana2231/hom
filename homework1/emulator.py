import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import zipfile
import sys
import argparse
from datetime import datetime

class ShellEmulator:
    def __init__(self, master, virtual_fs_path, hostname):
        self.master = master
        self.master.title("Shell Emulator")
        self.current_path = "/"
        self.history = []
        self.hostname = hostname

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.label = tk.Label(master, text=f"{self.hostname}")
        self.label.pack(padx=10, pady=5)

        self.entry = tk.Entry(master)
        self.entry.pack(padx=10, pady=10, fill=tk.X)
        self.entry.bind("<Return>", self.execute_command)

        self.extract_virtual_fs(virtual_fs_path)

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Запуск эмулятора командной строки.')
        parser.add_argument('--hostname', type=str, required=True, help='Имя компьютера для показа в приглашении к вводу.')
        parser.add_argument('virtual_fs', type=str, help='Путь к образу файловой системы (zip).')

        args = parser.parse_args()

        if not os.path.exists(args.virtual_fs):
            parser.error(f"Файл виртуальной файловой системы '{args.virtual_fs}' не найден.")
        
        return args

    def extract_virtual_fs(self, virtual_fs_path):
        if not os.path.exists(virtual_fs_path):
            messagebox.showerror("Ошибка", "Файл виртуальной файловой системы не найден.")
            return

        with zipfile.ZipFile(virtual_fs_path, 'r') as zip_ref:
            zip_ref.extractall("virtual_fs")

    def execute_command(self, event):
        command = self.entry.get()
        self.history.append(command)

        command_dict = {
            "ls": self.list_files,
            "cd": lambda: self.change_directory(command[3:]),
            "echo": lambda: self.echo_command(command[5:]),
            "date": self.print_date,
            "exit": self.master.quit,
            "history": self.show_history,
        }

        cmd_func = command_dict.get(command.split()[0], None)

        if cmd_func:
            cmd_func()
        else:
            self.text_area.insert(tk.END, f"{self.hostname}: команда не найдена\n")

        self.entry.delete(0, tk.END)

    def list_files(self):
        try:
            files = os.listdir(f"virtual_fs{self.current_path}")
            output = "\n".join(files) if files else "Пустая директория\n"
            self.text_area.insert(tk.END, f"{output}\n")
        except FileNotFoundError:
            self.text_area.insert(tk.END, "Директория не найдена\n")

    def change_directory(self, path):
        if path == "..":
            if self.current_path != "/":
                parts = self.current_path.split("/")
                parts.pop()
                self.current_path = "/".join(parts) or "/"
                return
        
        new_path = os.path.join(f"virtual_fs{self.current_path}", path)
        
        if os.path.isdir(new_path):
            self.current_path = new_path.replace("virtual_fs", "")
            return
        else:
            self.text_area.insert(tk.END, "Директория не найдена\n")

    def echo_command(self, message):
        self.text_area.insert(tk.END, f"{message}\n")
        return f"{message}\n"

    def print_date(self):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.text_area.insert(tk.END, f"{current_date}\n")

    def show_history(self):
        history_output = "\n".join(self.history) or "История пуста\n"
        self.text_area.insert(tk.END, f"История команд:\n{history_output}\n")

if __name__ == "__main__":
    args = ShellEmulator.parse_arguments()
    root = tk.Tk()
    app = ShellEmulator(root, args.virtual_fs, args.hostname)
    
    root.mainloop()
