# LiteOCR - Quick Screenshot OCR Tool

A fast OCR tool that uses large language models to convert screenshot text into Markdown format and copies it to clipboard.

## Features

- Quick screenshot capture with hotkey (Ctrl+Alt+S)
- Automatic recognition of math formulas, tables and text formatting
- Conversion to structured Markdown/LaTeX format
- Results automatically copied to clipboard
- System tray icon management

## Installation & Running

### Installation

```bash
uv sync
```

### Run the program

```bash
uv run src/main.py
```

## Usage

1. After running the program, an icon will appear in the system tray
2. Right-click the icon to view menu options:
   - "Settings": Configure API key and model name
   - "Exit": Quit the program
3. Use hotkey `Ctrl+Alt+S` to select screen area
4. The program will automatically process the screenshot and convert it, results will be copied to clipboard

## License

MIT License
