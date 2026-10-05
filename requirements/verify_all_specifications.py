#!/usr/bin/env python3
"""
Forwarding wrapper for backward compatibility.
Executes lint_all_specifications.py.
"""
import os, subprocess, sys

script_dir = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(script_dir, 'lint_all_specifications.py')
sys.exit(subprocess.call([sys.executable, target] + sys.argv[1:]))
