<div align="center">
  <img src="resources/icons/icon.png" width="128" height="128" alt="LiteOCR Icon">
</div>

<div align="center">
  <a href="README.md">English</a> |
  <a href="README_zh.md">中文</a>
</div>

# LiteOCR - 基于AI的 OCR 工具

这是一款基于AI的 OCR 工具。你可以使用快捷键捕捉屏幕内容，然后发送给大语言模型处理，自动转换为 Markdown 格式。处理完成的结果会自动复制到剪贴板，方便你直接粘贴到需要的地方。

## ✨ 功能特性

- **快速截图**: 使用可更改的快捷键快速捕捉屏幕区域。
- **智能识别**: 自动识别数学公式、表格和文本格式。
- **格式转换**: 使用AI识别图片并且转换为 Markdown/LaTeX 格式。
- **自动复制**: 结果自动复制到剪贴板。
- **系统托盘管理**: 便捷的系统托盘图标管理。

## 🚀 安装与运行

### 安装依赖

```bash
# 使用 pip 安装依赖
pip install -e .
# or 
# 使用 uv 安装依赖
uv sync
```

### 运行程序

如果你不想从源码运行程序，可以直接下载可执行文件。

前往 [Releases](https://github.com/zwldarren/LiteOCR/releases) 页面下载最新的可执行文件，双击运行 `liteocr.exe`。

### 从源码运行程序

```bash
# 使用 PySide6 生成资源文件
uv run pyside6-rcc resources/resources.qrc -o src/liteocr/resources_rc.py

# 运行程序
uv run liteocr
```

## 🛠️ 使用方法

1. 运行程序后，系统托盘区将出现一个图标。
2. 右键点击图标查看菜单选项：
   - "设置 (Settings)": 配置 API 密钥和模型名称。
   - "退出 (Exit)": 退出程序。
3. 使用快捷键 `Ctrl+Alt+S` 选择屏幕区域。
4. 程序将自动处理截图并进行转换，结果会自动复制到剪贴板。

## 📄 许可证 (License)

[MIT 许可证 (MIT License)](LICENSE)
