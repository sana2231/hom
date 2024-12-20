import unittest
from unittest.mock import patch, mock_open
import tkinter as tk
from emulator import ShellEmulator
import datetime
class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.emulator = ShellEmulator(self.root, "virtual_fs.zip", "test_host")

    @patch('os.listdir', return_value=['file1.txt', 'file2.txt'])
    def test_list_files(self, mock_listdir):
        self.emulator.list_files()
        self.assertIn("file1.txt", self.emulator.text_area.get("1.0", tk.END))
        self.assertIn("file2.txt", self.emulator.text_area.get("1.0", tk.END))

    @patch('os.path.isdir', return_value=True)
    def test_change_directory(self, mock_isdir):
        self.emulator.change_directory("subdir")
        self.assertEqual(self.emulator.current_path, "/subdir")

    @patch('os.path.isdir', return_value=False)
    def test_change_directory_not_found(self, mock_isdir):
        self.emulator.change_directory("nonexistent")
        self.assertIn("Директория не найдена", self.emulator.text_area.get("1.0", tk.END))

    def test_show_history(self):
        self.emulator.history = ["ls", "pwd", "cd subdir"]
        self.emulator.show_history()
        self.assertIn("ls\npwd\ncd subdir", self.emulator.text_area.get("1.0", tk.END))


    def test_echo_command(self):
        message = "Hello, World!"
        self.emulator.echo_command(message)
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn(message, output)

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
