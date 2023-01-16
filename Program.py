import importlib
import os
import platform
import sqlite3
import subprocess
import sys
import urllib.request

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TimeElapsedColumn,
)
from rich.rule import Rule

console = Console()
progress = Progress(
    SpinnerColumn(),
    *Progress.get_default_columns(),
    "|",
    TimeElapsedColumn(),
    console=console,
)

progress.start()


def download(url, name, filename, command):
    task = progress.add_task(f"[green]Downloading {name}")
    if os.path.exists(filename):
        progress.log(Rule(f"{name} Setup already exists!"))
    else:
        urllib.request.urlretrieve(url, filename, reporthook=lambda count, block_size, total_size: progress.update(
            task, completed=int(count * block_size * 100 / total_size)))

        progress.log(Rule(f"{name} downloaded successfully!"))
    install(name, command, task)


def install(name, command, task=None):
    if task is None:
        task = progress.add_task(f"[green]Installing {name} extension in VSCode", total=None)
        result = subprocess.run(["code", "--install-extension", command], capture_output=True)

    else:
        progress.update(task, description=f"[green]Installing {name}")
        result = subprocess.run([command], capture_output=True)

    if result.stderr:
        progress.log(f"[red]{result.stderr.decode()}")
    progress.log(result.stdout.decode())

    progress.log(Rule(f"{name} installed successfully!"))
    progress.update(task, visible=False)
    progress.stop_task(task)


def main():
    if platform.system() != "Windows":
        raise Exception("This program is only compatible with Windows")

    try:
        importlib.import_module("rich")
        importlib.import_module("bs4")
        progress.log("Required dependencies are already installed")
    except ImportError:
        try:
            subprocess.run(["pip", "install", "-U", "rich", "bs4"], check=True)
            progress.log("Required dependencies are installed")
        except subprocess.CalledProcessError as e:
            progress.log(f"An error occurred while installing the dependencies: {e}")
            progress.stop()
            sys.exit(1)

        progress.log("Required dependencies are installed")

    with sqlite3.connect("programs.db") as conn:
        cursor = conn.cursor()
        # TODO FIX: This is susceptible to SQL Injection Attack.
        cursor.execute("SELECT name, url, filename, args FROM programs")
        for name, url, filename, args in cursor.fetchall():
            download(url, name, filename, f"{filename} {args}")

        cursor.execute("SELECT name, id FROM extensions")
        for name, id in cursor.fetchall():
            install(name, id)

    progress.stop()