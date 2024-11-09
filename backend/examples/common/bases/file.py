import os
from datetime import datetime
from abc import ABC, abstractmethod
'''? Watcher'''

class FileBase(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.file_extn = os.path.splitext(file_path)[1]
        self._set_metadata(type = 'BASIC')    
    def _set_metadata(self, type):
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        file_info = os.stat(self.file_path)
        return {
            "type" : type,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "size": file_info.st_size,
            "created": datetime.fromtimestamp(file_info.st_ctime),
            "modified": datetime.fromtimestamp(file_info.st_mtime),
            "accessed": datetime.fromtimestamp(file_info.st_atime),
        }
    
    def exists(self):
        """Check if the file exists."""
        return os.path.exists(self.file_path)
    
    def delete(self):
        """Delete the file."""
        if self.exists():
            os.remove(self.file_path)
        else:
            print("File not found.")

    def change_owner(self):
        pass

    def find_files():
        pass
    
    @abstractmethod
    def content(self):
        """This should be implemented by subclasses, txt_file.content(), pdf_file.content(), docx, html, ..."""
        pass

    def __str__(self):
        return f"File({self.file_path})"


