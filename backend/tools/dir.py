# Write a wrapper class for File System to support multiple file systems
import os
from sys import platform
import shutil
from pathlib import Path
from typing import List, Union, Optional

class Dir:
    """A wrapper class for directory operations supporting multiple file systems"""
    
    def __init__(self, base_path: Union[str, Path]):
        self.base_path = Path(base_path)  # Convert base_path to a Path object if it isn’t already

        # Provide platform-specific logging or warnings
        if platform == 'aix':
            pass
        elif platform == 'android':
            pass
        elif platform == 'ios':
            pass
        elif platform == 'linux':
            pass
        elif platform == 'darwin':
            pass
        elif platform == 'win32':
            pass
        else:
            print(f"unknown platform: {self.base_path}")

    def create(self, path: Union[str, Path]) -> Path:
        """Create a new directory"""
        full_path = self.base_path / path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path
    
    def remove(self, path: Union[str, Path], recursive: bool = False) -> None:
        """Remove a directory"""
        full_path = self.base_path / path
        if recursive:
            shutil.rmtree(full_path)
        else:
            full_path.rmdir()
    
    def list_files(self, path: Optional[Union[str, Path]] = None) -> List[Path]:
        """List contents of a directory"""
        search_path = self.base_path
        if path:
            search_path = search_path / path
        return list(search_path.iterdir())
    
    def exists(self, path: Union[str, Path]) -> bool:
        """Check if directory exists"""
        return (self.base_path / path).exists()
    
    def is_directory(self, path: Union[str, Path]) -> bool:
        """Check if path is a directory"""
        '''
        Linux:
            obj = Dir("/home/user")
            print(obj.is_directory("documents"))  
            # Checks if /home/user/documents is a directory

        Windows:
            obj = Dir("C:\\Users\\YourUsername")
            print(obj.is_directory("Documents"))  
            # Checks if C:\Users\YourUsername\Documents is a directory
            print(obj.is_directory("D:\\OtherFolder"))  
            # Checks if D:\OtherFolder is a directory
        '''
        return (self.base_path / path).is_dir()
    
    def get_size(self, path: Optional[Union[str, Path]] = None) -> int:
        """Get total size of directory in bytes"""
        search_path = self.base_path
        if path:
            search_path = search_path / path
            
        total_size = 0
        for dirpath, _, filenames in os.walk(search_path):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                total_size += file_path.stat().st_size
        return total_size
    
    def copy_directory(self, src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Copy directory from source to destination"""
        src_path = self.base_path / src
        dst_path = self.base_path / dst
        shutil.copytree(src_path, dst_path)
