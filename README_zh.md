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

# LiteOCR - 快速截图 OCR 工具

一款 OCR 工具，使用大型语言模型将截图文本转换为 Markdown 格式并复制到剪贴板。

## ✨ 功能特性

- **快速截图**: 使用快捷键 (Ctrl+Alt+S) 快速捕捉屏幕区域。
- **智能识别**: 自动识别数学公式、表格和文本格式。
- **格式转换**: 转换为结构化的 Markdown/LaTeX 格式。
- **自动复制**: 结果自动复制到剪贴板。
- **系统托盘管理**: 便捷的系统托盘图标管理。

## 🚀 安装与运行

### 安装

```bash
uv sync
```

### 运行程序

```bash
uv run src/main.py
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
