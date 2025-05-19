uv sync --all-extras
uv run pyside6-rcc resources/resources.qrc -o src/liteocr/resources_rc.py
uv run nuitka --standalone --onefile --windows-console-mode=disable --windows-icon-from-ico=resources/icons/icon.png --enable-plugin=pyside6 src/liteocr/main.py -o LiteOCR.exe
