#!/usr/bin/env python3
"""
Example demonstrating the GUI features of question_maker
"""

def print_gui_features():
    """Display information about GUI features"""
    print("QUESTION MAKER GUI FEATURES")
    print("=" * 50)
    print()
    
    print("🖥️  USER INTERFACE:")
    print("   • Modern tabbed interface with Input, Results, and Settings tabs")
    print("   • Clean, intuitive design with status bar and progress indicators")
    print("   • Responsive layout that works on different screen sizes")
    print()
    
    print("📝 INPUT OPTIONS:")
    print("   • File Input: Browse and select text files (.txt, etc.)")
    print("   • URL Input: Process text from web pages")
    print("   • Direct Text: Type or paste text directly into the interface")
    print("   • Example Data: Load sample questions for testing")
    print()
    
    print("🔧 PROCESSING OPTIONS:")
    print("   • Basic Statistics: Word count, character count, averages")
    print("   • Multiple Choice Questions: Extract structured Q&A data")
    print("   • Sentence Extraction: Split text into individual sentences")
    print("   • Paragraph Extraction: Identify paragraph boundaries")
    print()
    
    print("📊 RESULTS DISPLAY:")
    print("   • Summary Statistics: Overview of processing results")
    print("   • Question Tree View: Browse extracted questions easily")
    print("   • Detailed View: See full question text and all options")
    print("   • Real-time Updates: Progress bars and status messages")
    print()
    
    print("💾 EXPORT OPTIONS:")
    print("   • JSON Export: Complete structured data for programming")
    print("   • CSV Export: Spreadsheet-compatible format")
    print("   • Text Export: Human-readable formatted text")
    print("   • Auto-Export: Automatically save results with timestamps")
    print()
    
    print("⚙️  ADVANCED FEATURES:")
    print("   • Multi-threading: Processing doesn't freeze the interface")
    print("   • Error Handling: Clear error messages and recovery")
    print("   • Configurable: Choose which processors to run")
    print("   • Cross-platform: Works on Windows, Mac, and Linux")
    print()
    
    print("🚀 HOW TO USE:")
    print("   1. Run: python run_gui.py")
    print("   2. Choose your input source (File/URL/Text)")
    print("   3. Configure processors in Settings tab")
    print("   4. Click 'Process Text' to analyze")
    print("   5. View results and export in desired format")
    print()
    
    print("📁 FILE LOCATIONS:")
    print("   • Main GUI: gui_app.py")
    print("   • Launcher: run_gui.py")
    print("   • Windows Batch: run_gui.bat")
    print("   • Exports: exports/ directory (auto-created)")
    print()


def demonstrate_programmatic_access():
    """Show how to use the GUI components programmatically"""
    print("PROGRAMMATIC GUI ACCESS")
    print("=" * 30)
    print()
    
    code_example = '''
# Example: Using GUI components in your own code
import tkinter as tk
from gui_app import QuestionMakerGUI

# Create and run the GUI
root = tk.Tk()
app = QuestionMakerGUI(root)
root.mainloop()

# Or integrate GUI components into existing applications
from gui_app import QuestionMakerGUI
# ... your existing code ...
gui_component = QuestionMakerGUI(your_existing_root)
'''
    
    print("Python Code:")
    print(code_example)


if __name__ == "__main__":
    print_gui_features()
    print("\n" + "="*50 + "\n")
    demonstrate_programmatic_access()
    
    print("\n" + "="*50)
    print("Ready to launch GUI? Run: python run_gui.py")
    print("Or double-click: run_gui.bat (Windows)")
    print("="*50)