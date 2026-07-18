#!/usr/bin/env python3
"""Universal auto-launcher for the Pell Grant Rip-Off Calculator.

One command on any OS:
    python3 start.py

First run: creates a private virtual environment in .venv/ inside this folder
and installs everything from requirements.txt into it (PyQt6 for the app,
pypdf for reading your audit PDF). Later runs reuse the venv and launch
straight away. Nothing is installed outside this project folder; delete
.venv/ to undo everything.

On macOS you can also just double-click start.command, which runs this file.
"""

import os
import subprocess
import sys
import venv

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(ROOT, ".venv")
VENV_PY = (os.path.join(VENV, "Scripts", "python.exe") if os.name == "nt"
           else os.path.join(VENV, "bin", "python"))


def fail(msg):
    sys.exit(f"\nERROR: {msg}\n")


def main():
    os.chdir(ROOT)
    if sys.version_info < (3, 9):
        fail("Python 3.9 or newer is required. Get it from https://www.python.org/downloads/")

    if not os.path.exists(VENV_PY):
        print("First run: creating a virtual environment in .venv/ ...")
        try:
            venv.create(VENV, with_pip=True)
        except Exception as e:
            fail(f"Couldn't create the virtual environment: {e}\n"
                 "On Debian/Ubuntu you may need: sudo apt install python3-venv")

    print("Installing/checking requirements (PyQt6, pypdf)...")
    subprocess.run([VENV_PY, "-m", "pip", "install", "--quiet", "--upgrade", "pip"])
    r = subprocess.run([VENV_PY, "-m", "pip", "install", "--quiet", "-r", "requirements.txt"])
    if r.returncode != 0:
        fail("Couldn't install requirements. Check your internet connection and run this again.")

    print("Launching the Pell Grant Rip-Off Calculator...")
    if os.name == "nt":
        sys.exit(subprocess.run([VENV_PY, "payment_calc.py"]).returncode)
    os.execv(VENV_PY, [VENV_PY, "payment_calc.py"])


if __name__ == "__main__":
    main()
