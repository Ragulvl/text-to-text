"""
Text-to-Text Generator Application
A simple GUI application for text transformation using Google Gemini API.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from gemini_helper import GeminiHelper


class TextGeneratorApp:
    """
    Main application class for the Text-to-Text Generator.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: The root Tkinter window
        """
        self.root = root
        self.root.title("Text-to-Text Generator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize Gemini helper with API key
        # Note: In production, you should load this from environment variables or config file
        self.api_key = "AIzaSyBJdKWXME2lCZjYMMZSx0oH3qLkBHEN0ME"
        self.gemini_helper = GeminiHelper(self.api_key)
        
        # Create the GUI components
        self.create_widgets()
    
    def create_widgets(self):
        """
        Create and arrange all GUI widgets.
        """
        # Title label
        title_label = tk.Label(
            self.root,
            text="Text-to-Text Generator",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Input section
        input_frame = tk.Frame(self.root, padx=20, pady=10)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        input_label = tk.Label(
            input_frame,
            text="Input Text:",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        input_label.pack(fill=tk.X, pady=(0, 5))
        
        # Text input box with scrollbar
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=10,
            wrap=tk.WORD,
            font=("Arial", 11)
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Operation selection and button frame
        control_frame = tk.Frame(self.root, padx=20, pady=10)
        control_frame.pack(fill=tk.X)
        
        # Dropdown for operation selection
        operation_label = tk.Label(
            control_frame,
            text="Operation:",
            font=("Arial", 11)
        )
        operation_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.operation_var = tk.StringVar(value="Summarize")
        operation_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.operation_var,
            values=["Summarize", "Rephrase", "Expand"],
            state="readonly",
            width=15,
            font=("Arial", 11)
        )
        operation_dropdown.pack(side=tk.LEFT, padx=(0, 20))
        
        # Generate button
        self.generate_button = tk.Button(
            control_frame,
            text="Generate",
            command=self.generate_text,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=5,
            cursor="hand2"
        )
        self.generate_button.pack(side=tk.LEFT)
        
        # Output section
        output_frame = tk.Frame(self.root, padx=20, pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        output_label = tk.Label(
            output_frame,
            text="Generated Output:",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        output_label.pack(fill=tk.X, pady=(0, 5))
        
        # Output text box with scrollbar
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=10,
            wrap=tk.WORD,
            font=("Arial", 11),
            state=tk.DISABLED
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def generate_text(self):
        """
        Handle the Generate button click event.
        """
        # Get input text
        user_input = self.input_text.get("1.0", tk.END).strip()
        
        # Check if input is empty
        if not user_input:
            messagebox.showwarning("Warning", "Please enter some text to process.")
            return
        
        # Get selected operation
        operation = self.operation_var.get()
        
        # Disable the button during generation
        self.generate_button.config(state=tk.DISABLED, text="Generating...")
        self.root.update()
        
        try:
            # Generate text using Gemini API
            result = self.gemini_helper.generate_text(user_input, operation)
            
            # Enable output text box and update it
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.config(state=tk.DISABLED)
            
        except Exception as e:
            # Show error message
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", f"Error: {str(e)}")
            self.output_text.config(state=tk.DISABLED)
        
        finally:
            # Re-enable the button
            self.generate_button.config(state=tk.NORMAL, text="Generate")
            self.root.update()


def main():
    """
    Main function to run the application.
    """
    root = tk.Tk()
    app = TextGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

