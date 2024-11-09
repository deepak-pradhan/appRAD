from backend.examples.common.bases.file import FileBase

class TextFile(FileBase):

    def __init__(self):
        super().__init__(self)
        if not self.exists(self):
            print('Error:404')
        
    def content(self):
        with open(self.file_path, 'r') as file:
            text = file.read()
        return text   
