from pathlib import Path
import os
import shutil
from typing import List, Union, Generator
import stat

class FileSystemBase:
    def __init__(self, root_path: Union[str, Path]):
        self.root = Path(root_path).resolve()
        
    def create_directory(self, path: Union[str, Path]) -> Path:
        full_path = self.root / Path(path)
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path
    
    def list_directory(self, path: Union[str, Path] = ".") -> Generator[Path, None, None]:
        target_path = self.root / Path(path)
        return target_path.glob("*")
    
    def remove(self, path: Union[str, Path], force: bool = False) -> bool:
        target = self.root / Path(path)
        if target.is_file():
            if force:
                os.chmod(target, stat.S_IWRITE)
            target.unlink()
        elif target.is_dir():
            if force:
                for p in target.rglob("*"):
                    os.chmod(p, stat.S_IWRITE)
            shutil.rmtree(target)
        return True
    
    def move(self, src: Union[str, Path], dst: Union[str, Path]) -> Path:
        source = self.root / Path(src)
        destination = self.root / Path(dst)
        destination.parent.mkdir(parents=True, exist_ok=True)
        return Path(shutil.move(str(source), str(destination)))
    
    def copy(self, src: Union[str, Path], dst: Union[str, Path]) -> Path:
        source = self.root / Path(src)
        destination = self.root / Path(dst)
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        if source.is_file():
            return Path(shutil.copy2(str(source), str(destination)))
        return Path(shutil.copytree(str(source), str(destination)))