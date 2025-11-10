# Text-to-Text Generator - Git Repository Description

A lightweight Python GUI application that leverages Google's Gemini AI API to transform text through three powerful operations: summarization, rephrasing, and expansion. Built with Tkinter for a clean, user-friendly interface, this tool makes AI-powered text transformation accessible to everyone.

## Key Features

The application provides three core text transformation capabilities:
- **Summarize**: Condense lengthy text into concise summaries while preserving key information
- **Rephrase**: Rewrite text with different wording while maintaining the original meaning and context
- **Expand**: Enhance text with additional details, explanations, and comprehensive information

## Technical Highlights

- **Clean Architecture**: Modular design with separate API integration module (`gemini_helper.py`) for maintainability
- **Smart Error Handling**: Automatic model fallback system and user-friendly error messages for quota limits and API issues
- **Beginner-Friendly**: Well-commented code suitable for learning Python GUI development and API integration
- **Cross-Platform**: Works on Windows, macOS, and Linux with Python 3.7+

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`
2. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Add your API key to `main.py`
4. Run: `python main.py`

## Project Structure

- `main.py` - Main GUI application with Tkinter
- `gemini_helper.py` - Gemini API integration with intelligent error handling
- `requirements.txt` - Python dependencies
- `README.md` - Comprehensive setup and usage guide

Perfect for students learning Python GUI development, developers needing quick text transformation tools, or anyone wanting to explore Google's Gemini API capabilities.

