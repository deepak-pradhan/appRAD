import fitz
from backend.examples.common.bases.file import FileBase


class PDFFile(FileBase):

    def __init__(self):
        super().__init__(self)
        if not self.exists(self):
            print('Error:404')

    def content(pdf_path):
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        
    def ocr(self):
        pass
