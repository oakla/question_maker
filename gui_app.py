#!/usr/bin/env python3
"""
GUI Application for question_maker - Multiple Choice Question Extractor
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
from pathlib import Path
from datetime import datetime
import threading
import webbrowser

from question_maker import TextTransformer
from question_maker.text_transformer import (
    basic_stats_processor,
    extract_multiple_choice_questions,
    extract_sentences,
    extract_paragraphs
)


class QuestionMakerGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.setup_layout()
        
        # Initialize transformer
        self.transformer = TextTransformer()
        self.setup_processors()
        
        # Results storage
        self.current_result = None
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Question Maker - Multiple Choice Question Extractor")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set icon (if available)
        try:
            # You can add an icon file here
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
    
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.source_type = tk.StringVar(value="file")
        self.input_text = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Processor options
        self.use_basic_stats = tk.BooleanVar(value=True)
        self.use_mc_questions = tk.BooleanVar(value=True)
        self.use_sentences = tk.BooleanVar(value=False)
        self.use_paragraphs = tk.BooleanVar(value=False)
        
        # Export settings
        self.export_location = tk.StringVar(value=str(Path("exports").absolute()))
    
    def setup_processors(self):
        """Setup text processors based on user selection"""
        self.transformer.processors.clear()
        
        if self.use_basic_stats.get():
            self.transformer.add_processor(basic_stats_processor)
        if self.use_mc_questions.get():
            self.transformer.add_processor(extract_multiple_choice_questions)
        if self.use_sentences.get():
            self.transformer.add_processor(extract_sentences)
        if self.use_paragraphs.get():
            self.transformer.add_processor(extract_paragraphs)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Input tab
        self.input_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.input_frame, text="Input")
        self.create_input_tab()
        
        # Results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        self.create_results_tab()
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar()
    
    def create_input_tab(self):
        """Create the input tab with source selection"""
        # Main container
        main_container = ttk.Frame(self.input_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_container, text="Multiple Choice Question Extractor", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Source type selection
        source_frame = ttk.LabelFrame(main_container, text="Select Input Source", padding=10)
        source_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Radio buttons for source type
        ttk.Radiobutton(source_frame, text="File", variable=self.source_type, 
                       value="file", command=self.on_source_change).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(source_frame, text="URL", variable=self.source_type, 
                       value="url", command=self.on_source_change).pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(source_frame, text="Text Input", variable=self.source_type, 
                       value="string", command=self.on_source_change).pack(side=tk.LEFT, padx=10)
        
        # Input section
        input_section = ttk.LabelFrame(main_container, text="Input", padding=10)
        input_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # File input frame
        self.file_frame = ttk.Frame(input_section)
        self.file_frame.pack(fill=tk.X, pady=5)
        
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.input_text, 
                                   font=('Consolas', 10))
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.browse_button = ttk.Button(self.file_frame, text="Browse...", 
                                       command=self.browse_file)
        self.browse_button.pack(side=tk.RIGHT)
        
        # URL input frame
        self.url_frame = ttk.Frame(input_section)
        self.url_entry = ttk.Entry(self.url_frame, textvariable=self.input_text,
                                  font=('Consolas', 10))
        self.url_entry.pack(fill=tk.X, pady=5)
        
        # Text input frame
        self.text_frame = ttk.Frame(input_section)
        
        text_label = ttk.Label(self.text_frame, text="Enter or paste your text:")
        text_label.pack(anchor=tk.W)
        
        self.text_input = scrolledtext.ScrolledText(self.text_frame, height=15, 
                                                   font=('Consolas', 10))
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Control buttons
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="Process Text", 
                                        command=self.process_text, style='Accent.TButton')
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear", 
                                      command=self.clear_input)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.example_button = ttk.Button(button_frame, text="Load Example", 
                                        command=self.load_example)
        self.example_button.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(main_container, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))
        
        # Initially show file input
        self.on_source_change()
    
    def create_results_tab(self):
        """Create the results tab"""
        # Main container
        results_container = ttk.Frame(self.results_frame)
        results_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Results summary
        summary_frame = ttk.LabelFrame(results_container, text="Summary", padding=10)
        summary_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.summary_text = tk.Text(summary_frame, height=6, font=('Consolas', 10),
                                   state=tk.DISABLED, bg='#f0f0f0')
        self.summary_text.pack(fill=tk.X)
        
        # Questions display
        questions_frame = ttk.LabelFrame(results_container, text="Extracted Questions", padding=10)
        questions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Questions tree view with hidden column for data storage
        self.questions_tree = ttk.Treeview(questions_frame, columns=('question', 'options', 'full_question'), 
                                          show='tree headings', height=10)
        self.questions_tree.heading('#0', text='#')
        self.questions_tree.heading('question', text='Question')
        self.questions_tree.heading('options', text='Options')
        
        self.questions_tree.column('#0', width=50, minwidth=50)
        self.questions_tree.column('question', width=400, minwidth=200)
        self.questions_tree.column('options', width=100, minwidth=100)
        self.questions_tree.column('full_question', width=0, minwidth=0)  # Hidden column for data
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(questions_frame, orient=tk.VERTICAL, 
                                   command=self.questions_tree.yview)
        self.questions_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.questions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Question detail view
        detail_frame = ttk.LabelFrame(results_container, text="Question Details", padding=10)
        detail_frame.pack(fill=tk.X)
        
        self.detail_text = scrolledtext.ScrolledText(detail_frame, height=8, 
                                                    font=('Consolas', 10),
                                                    state=tk.DISABLED)
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # Export buttons
        export_frame = ttk.Frame(results_container)
        export_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(export_frame, text="Export JSON", 
                  command=self.export_json).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(export_frame, text="Export CSV", 
                  command=self.export_csv).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(export_frame, text="Export Text", 
                  command=self.export_text).pack(side=tk.LEFT)
        
        # Bind tree selection
        self.questions_tree.bind('<<TreeviewSelect>>', self.on_question_select)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_container = ttk.Frame(self.settings_frame)
        settings_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Processors section
        processors_frame = ttk.LabelFrame(settings_container, text="Text Processors", padding=10)
        processors_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Checkbutton(processors_frame, text="Basic Statistics (word count, etc.)", 
                       variable=self.use_basic_stats).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(processors_frame, text="Multiple Choice Questions", 
                       variable=self.use_mc_questions).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(processors_frame, text="Extract Sentences", 
                       variable=self.use_sentences).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(processors_frame, text="Extract Paragraphs", 
                       variable=self.use_paragraphs).pack(anchor=tk.W, pady=2)
        
        # Output settings
        output_frame = ttk.LabelFrame(settings_container, text="Output Settings", padding=10)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.auto_export = tk.BooleanVar(value=False)
        ttk.Checkbutton(output_frame, text="Auto-export results to files", 
                       variable=self.auto_export).pack(anchor=tk.W, pady=2)
        
        # Export location setting
        export_location_frame = ttk.Frame(output_frame)
        export_location_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(export_location_frame, text="Export location:").pack(anchor=tk.W)
        
        location_input_frame = ttk.Frame(export_location_frame)
        location_input_frame.pack(fill=tk.X, pady=(2, 0))
        
        self.export_location_entry = ttk.Entry(location_input_frame, textvariable=self.export_location,
                                             font=('Consolas', 9))
        self.export_location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Button frame for browse and reset
        button_frame = ttk.Frame(location_input_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="Browse...", 
                  command=self.browse_export_location).pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(button_frame, text="Reset", 
                  command=self.reset_export_location).pack(side=tk.LEFT)
        
        # Help text and quick access
        help_frame = ttk.Frame(export_location_frame)
        help_frame.pack(fill=tk.X, pady=(2, 0))
        
        help_label = ttk.Label(help_frame, 
                              text="Files will be saved to this directory when using manual or auto-export",
                              font=('Arial', 8), foreground='gray')
        help_label.pack(side=tk.LEFT)
        
        ttk.Button(help_frame, text="Open Folder", 
                  command=self.open_export_folder).pack(side=tk.RIGHT)
        
        # About section
        about_frame = ttk.LabelFrame(settings_container, text="About", padding=10)
        about_frame.pack(fill=tk.X)
        
        about_text = """Question Maker - Multiple Choice Question Extractor
Version 1.0

This application extracts multiple-choice questions from text using advanced 
text processing algorithms. It supports files, URLs, and direct text input.

Features:
• Automatic question detection
• Support for A-E option formats
• Multiple export formats (JSON, CSV, Text)
• Comprehensive text analysis
• User-friendly interface"""
        
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.LEFT)
        about_label.pack(anchor=tk.W)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_text, 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
    
    def setup_layout(self):
        """Setup the main layout"""
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def on_source_change(self):
        """Handle source type change"""
        source = self.source_type.get()
        
        # Hide all frames
        self.file_frame.pack_forget()
        self.url_frame.pack_forget()
        self.text_frame.pack_forget()
        
        # Show appropriate frame
        if source == "file":
            self.file_frame.pack(fill=tk.X, pady=5)
        elif source == "url":
            self.url_frame.pack(fill=tk.X, pady=5)
        elif source == "string":
            self.text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Clear input
        self.input_text.set("")
        if hasattr(self, 'text_input'):
            self.text_input.delete('1.0', tk.END)
    
    def browse_file(self):
        """Open file browser"""
        filetypes = [
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select text file",
            filetypes=filetypes
        )
        
        if filename:
            self.input_text.set(filename)
    
    def browse_export_location(self):
        """Open directory browser for export location"""
        directory = filedialog.askdirectory(
            title="Select export directory",
            initialdir=self.export_location.get()
        )
        
        if directory:
            # Validate directory is writable
            try:
                Path(directory).mkdir(parents=True, exist_ok=True)
                # Test write access
                test_file = Path(directory) / ".test_write_access"
                test_file.touch()
                test_file.unlink()
                
                self.export_location.set(directory)
                self.status_text.set(f"Export location set to: {os.path.basename(directory)}")
            except (PermissionError, OSError) as e:
                messagebox.showerror("Permission Error", 
                                   f"Cannot write to selected directory:\n{directory}\n\nError: {e}")
                self.status_text.set("Export location change failed - permission denied")
    
    def reset_export_location(self):
        """Reset export location to default"""
        default_location = str(Path("exports").absolute())
        self.export_location.set(default_location)
        self.status_text.set("Export location reset to default")
    
    def open_file_location(self, filename):
        """Open the folder containing the exported file"""
        try:
            import subprocess
            import platform
            
            folder_path = os.path.dirname(os.path.abspath(filename))
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", folder_path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            else:  # Linux and others
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            print(f"Could not open file location: {e}")
            # Fallback: just show a message with the path
            messagebox.showinfo("File Location", f"File saved to:\n{folder_path}")
    
    def open_export_folder(self):
        """Open the current export directory"""
        try:
            export_dir = Path(self.export_location.get())
            export_dir.mkdir(parents=True, exist_ok=True)  # Ensure it exists
            self.open_file_location(str(export_dir / "dummy"))  # Use dummy file to get folder
        except Exception as e:
            messagebox.showerror("Error", f"Could not open export folder:\n{e}")
    
    def clear_input(self):
        """Clear all input"""
        self.input_text.set("")
        if hasattr(self, 'text_input'):
            self.text_input.delete('1.0', tk.END)
        self.clear_results()
    
    def load_example(self):
        """Load example text"""
        example_text = """Which of the following is an essential amino acid in humans?
A Tyrosine
B Glutamine
C Glutamate
D Phenylalanine
E Lysine

What is the capital of France?
A London
B Paris
C Berlin
D Madrid

Which programming language is this application written in?
A Java
B Python
C JavaScript
D C++"""
        
        if self.source_type.get() == "string":
            self.text_input.delete('1.0', tk.END)
            self.text_input.insert('1.0', example_text)
        else:
            # Switch to text input and load example
            self.source_type.set("string")
            self.on_source_change()
            self.text_input.delete('1.0', tk.END)
            self.text_input.insert('1.0', example_text)
    
    def process_text(self):
        """Process the text input"""
        # Get input based on source type
        source_type = self.source_type.get()
        
        if source_type == "file":
            input_data = self.input_text.get().strip()
            if not input_data:
                messagebox.showerror("Error", "Please select a file")
                return
            if not os.path.exists(input_data):
                messagebox.showerror("Error", "File does not exist")
                return
        elif source_type == "url":
            input_data = self.input_text.get().strip()
            if not input_data:
                messagebox.showerror("Error", "Please enter a URL")
                return
            if not (input_data.startswith('http://') or input_data.startswith('https://')):
                messagebox.showerror("Error", "Please enter a valid URL (starting with http:// or https://)")
                return
        elif source_type == "string":
            input_data = self.text_input.get('1.0', tk.END).strip()
            if not input_data:
                messagebox.showerror("Error", "Please enter some text")
                return
        
        # Setup processors
        self.setup_processors()
        
        if not self.transformer.processors:
            messagebox.showerror("Error", "Please select at least one processor in Settings")
            return
        
        # Process in separate thread
        self.start_processing()
        threading.Thread(target=self._process_worker, args=(input_data, source_type), 
                        daemon=True).start()
    
    def start_processing(self):
        """Start processing animation"""
        self.process_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.status_text.set("Processing...")
    
    def stop_processing(self):
        """Stop processing animation"""
        self.process_button.config(state=tk.NORMAL)
        self.progress_bar.stop()
    
    def _process_worker(self, input_data, source_type):
        """Worker thread for processing"""
        try:
            # Process the text
            result = self.transformer.transform(input_data, source_type)
            
            # Update UI in main thread
            self.root.after(0, self._process_complete, result)
            
        except Exception as e:
            # Handle errors in main thread
            self.root.after(0, self._process_error, str(e))
    
    def _process_complete(self, result):
        """Handle successful processing"""
        self.stop_processing()
        self.current_result = result
        self.display_results(result)
        self.status_text.set("Processing complete")
        
        # Switch to results tab
        self.notebook.select(self.results_frame)
        
        # Auto-export if enabled
        if self.auto_export.get():
            self.auto_export_results()
    
    def _process_error(self, error_msg):
        """Handle processing error"""
        self.stop_processing()
        self.status_text.set("Error occurred")
        messagebox.showerror("Processing Error", f"An error occurred while processing:\n\n{error_msg}")
    
    def display_results(self, result):
        """Display results in the results tab"""
        # Clear previous results
        self.clear_results()
        
        # Display summary
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete('1.0', tk.END)
        
        data = result.extracted_data
        summary = f"""Source: {result.source}
Processing Time: {result.timestamp}
Content Length: {len(result.content):,} characters

Statistics:
"""
        
        if 'word_count' in data:
            summary += f"  Words: {data['word_count']:,}\n"
        if 'sentence_count' in data:
            summary += f"  Sentences: {data['sentence_count']:,}\n"
        if 'paragraph_count' in data:
            summary += f"  Paragraphs: {data['paragraph_count']:,}\n"
        if 'question_count' in data:
            summary += f"  Questions Found: {data['question_count']:,}\n"
            summary += f"  Questions with Options: {data.get('questions_with_options', 0):,}\n"
        
        self.summary_text.insert('1.0', summary)
        self.summary_text.config(state=tk.DISABLED)
        
        # Display questions in tree
        if 'multiple_choice_questions' in data:
            questions = data['multiple_choice_questions']
            for i, question in enumerate(questions, 1):
                option_count = len(question.get('options', {}))
                item_id = self.questions_tree.insert('', 'end', text=str(i),
                                                    values=(question['question'][:60] + '...', 
                                                           f"{option_count} options"))
                # Store full question data
                self.questions_tree.set(item_id, 'full_question', json.dumps(question))
    
    def clear_results(self):
        """Clear all results"""
        # Clear summary
        if hasattr(self, 'summary_text'):
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.delete('1.0', tk.END)
            self.summary_text.config(state=tk.DISABLED)
        
        # Clear questions tree
        if hasattr(self, 'questions_tree'):
            for item in self.questions_tree.get_children():
                self.questions_tree.delete(item)
        
        # Clear detail view
        if hasattr(self, 'detail_text'):
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete('1.0', tk.END)
            self.detail_text.config(state=tk.DISABLED)
    
    def on_question_select(self, event):
        """Handle question selection in tree"""
        selection = self.questions_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        question_json = self.questions_tree.set(item, 'full_question')
        
        if question_json:
            question = json.loads(question_json)
            
            # Display question details
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete('1.0', tk.END)
            
            detail = f"Question: {question['question']}\n\n"
            detail += "Options:\n"
            
            for label in sorted(question.get('options', {}).keys()):
                detail += f"  {label}. {question['options'][label]}\n"
            
            detail += f"\nQuestion Number: {question.get('question_number', 'N/A')}\n"
            detail += f"Text Position: {question.get('start_position', 0)}-{question.get('end_position', 0)}"
            
            self.detail_text.insert('1.0', detail)
            self.detail_text.config(state=tk.DISABLED)
    
    def export_json(self):
        """Export results as JSON"""
        if not self.current_result:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        # Ensure export directory exists
        export_dir = Path(self.export_location.get())
        export_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            title="Save JSON Results",
            initialdir=str(export_dir),
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.current_result.to_dict(), f, indent=2, ensure_ascii=False)
                
                # Show success message with option to open folder
                result = messagebox.askyesno("Export Successful", 
                                           f"JSON file saved successfully:\n{filename}\n\nOpen containing folder?")
                if result:
                    self.open_file_location(filename)
                
                self.status_text.set(f"Exported JSON to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export JSON:\n{e}")
    
    def export_csv(self):
        """Export results as CSV"""
        if not self.current_result or 'multiple_choice_questions' not in self.current_result.extracted_data:
            messagebox.showwarning("No Results", "No questions to export")
            return
        
        # Ensure export directory exists
        export_dir = Path(self.export_location.get())
        export_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            title="Save CSV Results",
            initialdir=str(export_dir),
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import csv
                questions = self.current_result.extracted_data['multiple_choice_questions']
                
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Question_Number', 'Question_Text', 'Option_A', 'Option_B', 
                                   'Option_C', 'Option_D', 'Option_E', 'Start_Position', 'End_Position'])
                    
                    for question in questions:
                        options = question.get('options', {})
                        row = [
                            question.get('question_number', ''),
                            question['question'],
                            options.get('A', ''),
                            options.get('B', ''),
                            options.get('C', ''),
                            options.get('D', ''),
                            options.get('E', ''),
                            question.get('start_position', ''),
                            question.get('end_position', '')
                        ]
                        writer.writerow(row)
                
                # Show success message with option to open folder
                result = messagebox.askyesno("Export Successful", 
                                           f"CSV file saved successfully:\n{filename}\n\nOpen containing folder?")
                if result:
                    self.open_file_location(filename)
                
                self.status_text.set(f"Exported CSV to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export CSV:\n{e}")
    
    def export_text(self):
        """Export results as formatted text"""
        if not self.current_result:
            messagebox.showwarning("No Results", "No results to export")
            return
        
        # Ensure export directory exists
        export_dir = Path(self.export_location.get())
        export_dir.mkdir(parents=True, exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            title="Save Text Results",
            initialdir=str(export_dir),
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("QUESTION MAKER - EXTRACTED RESULTS\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Write summary
                    data = self.current_result.extracted_data
                    f.write(f"Source: {self.current_result.source}\n")
                    f.write(f"Processing Time: {self.current_result.timestamp}\n")
                    f.write(f"Content Length: {len(self.current_result.content):,} characters\n\n")
                    
                    if 'multiple_choice_questions' in data:
                        questions = data['multiple_choice_questions']
                        f.write(f"EXTRACTED QUESTIONS ({len(questions)} found):\n")
                        f.write("-" * 30 + "\n\n")
                        
                        for i, question in enumerate(questions, 1):
                            f.write(f"{i}. {question['question']}\n")
                            for label in sorted(question.get('options', {}).keys()):
                                f.write(f"   {label}) {question['options'][label]}\n")
                            f.write("\n")
                
                # Show success message with option to open folder
                result = messagebox.askyesno("Export Successful", 
                                           f"Text file saved successfully:\n{filename}\n\nOpen containing folder?")
                if result:
                    self.open_file_location(filename)
                
                self.status_text.set(f"Exported text to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export text:\n{e}")
    
    def auto_export_results(self):
        """Auto-export results to timestamped files"""
        if not self.current_result:
            return
        
        # Use selected export directory
        export_dir = Path(self.export_location.get())
        export_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            # Export JSON
            json_file = export_dir / f"results_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_result.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Export CSV if questions exist
            if 'multiple_choice_questions' in self.current_result.extracted_data:
                csv_file = export_dir / f"questions_{timestamp}.csv"
                questions = self.current_result.extracted_data['multiple_choice_questions']
                
                import csv
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Question_Number', 'Question_Text', 'Option_A', 'Option_B', 
                                   'Option_C', 'Option_D', 'Option_E'])
                    
                    for question in questions:
                        options = question.get('options', {})
                        row = [
                            question.get('question_number', ''),
                            question['question'],
                            options.get('A', ''),
                            options.get('B', ''),
                            options.get('C', ''),
                            options.get('D', ''),
                            options.get('E', '')
                        ]
                        writer.writerow(row)
            
            self.status_text.set(f"Auto-exported to {export_dir.name}/ directory")
            
        except Exception as e:
            print(f"Auto-export error: {e}")
            self.status_text.set("Auto-export failed")


def main():
    """Main application entry point"""
    root = tk.Tk()
    
    # Try to use modern ttk theme
    try:
        style = ttk.Style()
        # Use a modern theme if available
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
    except:
        pass
    
    app = QuestionMakerGUI(root)
    
    # Center window on screen
    root.eval('tk::PlaceWindow . center')
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()