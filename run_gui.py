#!/usr/bin/env python3
"""
Launcher script for the Question Maker GUI application
"""

import sys
import os

# Add the project root to Python path so we can import question_maker
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the GUI
from gui_app import main

if __name__ == "__main__":
    main()