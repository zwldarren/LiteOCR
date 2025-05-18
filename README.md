<div align="center">
  <svg width="128" height="128" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" rx="40" fill="#1565C0" />
    <rect x="78" y="68" width="100" height="120" rx="8" fill="#F5F5F5" />
    <rect x="90" y="88" width="76" height="6" rx="3" fill="#1565C0" />
    <rect x="90" y="104" width="76" height="6" rx="3" fill="#1565C0" />
    <rect x="90" y="120" width="60" height="6" rx="3" fill="#1565C0" />
    <rect x="78" y="135" width="100" height="3" fill="#1565C0" opacity="0.7" />
    <rect x="170" y="134" width="5" height="5" rx="2.5" fill="#FFFFFF" />
    <rect x="78" y="134" width="5" height="5" rx="2.5" fill="#FFFFFF" />
    <text x="128" y="218" font-family="Arial, sans-serif" font-size="24" font-weight="bold"
      text-anchor="middle" fill="white">LiteOCR</text>
  </svg>
</div>

# LiteOCR - Quick Screenshot OCR Tool

An OCR tool that uses large language models to convert screenshot text into Markdown format and copies it to the clipboard.

## ✨ Features

- **Quick Screenshot**: Use the hotkey (Ctrl+Alt+S) to quickly capture a screen area.
- **Intelligent Recognition**: Automatically recognizes mathematical formulas, tables, and text formatting.
- **Format Conversion**: Converts to structured Markdown/LaTeX format.
- **Auto Copy**: Results are automatically copied to the clipboard.
- **System Tray Management**: Convenient system tray icon for management.

## 🚀 Installation and Usage

### Installation

```bash
uv sync
```

### Running the Program

```bash
uv run src/main.py
```

## 🛠️ How to Use

1. After running the program, an icon will appear in the system tray.
2. Right-click the icon to see menu options:
   - "Settings": Configure API key and model name.
   - "Exit": Exit the program.
3. Use the hotkey `Ctrl+Alt+S` to select a screen area.
4. The program will automatically process the screenshot and perform the conversion. The result will be automatically copied to the clipboard.

## 📄 License

[MIT License](LICENSE)
