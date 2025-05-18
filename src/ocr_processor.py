from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import base64
from PySide6 import QtCore
from pydantic import SecretStr


class OCRProcessor:
    def __init__(self, api_key: str, model: str = "gpt-4.1-mini", base_url: str = ""):
        self.api_key = SecretStr(api_key)
        self.model = model
        self.base_url = base_url
        self.prompt = """
Convert the image content to clean LaTeX format. 
STRICTLY ONLY return the raw LaTeX code - no:
- Explanations
- Error messages
- Markdown code blocks
- Document templates
- Any other text
"""

    def process_image(self, screenshot_pixmap: bytes) -> str:
        """Process image from URL and return LaTeX text"""
        if not self.api_key:
            raise ValueError("API key is not configured")

        try:
            image_data = base64.b64encode(screenshot_pixmap).decode("utf-8")

            model = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                base_url=self.base_url,
                temperature=0.1,
                max_completion_tokens=8000,
            )

            prompt_template = ChatPromptTemplate(
                [
                    {"role": "user", "content": self.prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source_type": "base64",
                                "mime_type": "image/jpeg",
                                "data": "{image_data}",
                            }
                        ],
                    },
                ]
            )

            chain = prompt_template | model
            response = chain.invoke({"image_data": image_data})
            return response.text()
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
