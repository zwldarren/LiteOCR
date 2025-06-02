import base64
import ollama
from openai import OpenAI
from PySide6 import QtCore


class OCRProcessor:
    def __init__(
        self,
        provider: str,
        api_key: str = "",
        model: str = "gpt-4.1-mini",
        base_url: str = "",
    ):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.prompt = """
Convert the image content to structured Markdown with these guidelines:  
1. **Mathematical Formulas**:  
   - Inline equations: `$...$`  
   - Block equations: `$$...$$`  
   - Preserve symbols/notation exactly  

2. **Tables**:  
   - Use Markdown table syntax with alignment indicators (`:---`, `:---:`, `---:`)  
   - If unclear, infer columns/rows from content  
   - Add `<!-- Uncertain table structure -->` if formatting is ambiguous  

3. **Text Formatting**:  
   - Use `**bold**` and `*italic*` when visually evident  
   - Preserve numbered/bulleted lists  

4. **Unclear Content**:  
   - Keep raw text without formatting if ambiguous  
   - Add `<!-- Unclear content: ... -->` comments for uncertain sections  

5. **Code/Equations**:  
   - Use ` ``` ` blocks for code snippets  
   - Combine with LaTeX for annotated equations  

STRICTLY return ONLY raw Markdown text - no explanations, wrappers, Markdown code block or non-Markdown elements.
"""

    def process_image(self, screenshot_pixmap: bytes) -> str:
        """Process image from URL and return LaTeX text"""
        try:
            image_data = base64.b64encode(screenshot_pixmap).decode("utf-8")

            if self.provider == "openai":
                self.base_url = "https://api.openai.com/v1"
            elif self.provider == "gemini":
                self.base_url = (
                    "https://generativelanguage.googleapis.com/v1beta/openai/"
                )
            elif self.provider == "ollama":
                base_url = self.base_url if self.base_url else "http://localhost:11434"
                client = ollama.Client(host=base_url)

                response: ollama.ChatResponse = ollama.chat(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": self.prompt,
                            "images": [image_data],
                        },
                    ],
                )
                return response.message.content

            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )

            message = [
                {"role": "user", "content": self.prompt},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}",
                                "detail": "auto",
                            },
                        }
                    ],
                },
            ]

            response = client.chat.completions.create(
                model=self.model,
                messages=message,
                temperature=0.1,
                max_completion_tokens=8000,
            )
            text = response.choices[0].message.content
            return text
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")

    def image_to_bytes(self, image) -> bytes:
        """Convert QPixmap to bytes"""
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.OpenModeFlag.ReadWrite)
        image.save(buffer, "PNG")
        byte_array = buffer.data()

        # # Save debug image
        # timestamp = QtCore.QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        # debug_path = f"debug_screenshot_{timestamp}.png"
        # image.save(debug_path, "PNG")

        return bytes(byte_array.data())
