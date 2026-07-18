#!/bin/bash
# macOS double-click launcher. All the real logic is in start.py.
cd "$(dirname "$0")" || exit 1
exec python3 start.py
