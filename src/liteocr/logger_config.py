import logging
import os


class ErrorFileHandler(logging.Handler):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.file_handler = None
        self.log_dir = "logs"
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)
            if self.file_handler is None:
                self.file_handler = logging.FileHandler(self.filename)
                self.file_handler.setFormatter(self.formatter)
            self.file_handler.emit(record)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(), ErrorFileHandler("logs/liteocr_error.log")],
    )
