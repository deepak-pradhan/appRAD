import mmap
from pathlib import Path
from typing import Union, Any, BinaryIO
import json
import pickle

class FileHandlerBase:
    def __init__(self, encoding: str = 'utf-8'):
        self.encoding = encoding
    
    def read_text(self, path: Union[str, Path]) -> str:
        with open(path, 'r', encoding=self.encoding) as f:
            return f.read()
    
    def write_text(self, path: Union[str, Path], content: str) -> int:
        with open(path, 'w', encoding=self.encoding) as f:
            return f.write(content)
    
    def read_binary(self, path: Union[str, Path]) -> bytes:
        with open(path, 'rb') as f:
            return f.read()
    
    def write_binary(self, path: Union[str, Path], content: bytes) -> int:
        with open(path, 'wb') as f:
            return f.write(content)
    
    def read_json(self, path: Union[str, Path]) -> Any:
        with open(path, 'r', encoding=self.encoding) as f:
            return json.load(f)
    
    def write_json(self, path: Union[str, Path], content: Any, pretty: bool = True) -> None:
        with open(path, 'w', encoding=self.encoding) as f:
            json.dump(content, f, indent=2 if pretty else None)
    
    def read_pickle(self, path: Union[str, Path]) -> Any:
        with open(path, 'rb') as f:
            return pickle.load(f)
    
    def write_pickle(self, path: Union[str, Path], content: Any) -> None:
        with open(path, 'wb') as f:
            pickle.dump(content, f)

    def write_binary_fast(self, path: Union[str, Path], content: bytes, threshold: int = 100_000_000) -> None:
        """Fast binary write using mmap for large files"""
        if len(content) < threshold:
            return self.write_binary(path, content)
            
        with open(path, 'wb') as f:
            f.write(b'\0' * len(content))
            f.flush()
            with mmap.mmap(f.fileno(), len(content), access=mmap.ACCESS_WRITE) as mm:
                mm.write(content)
                mm.flush()

    def write_optimized(self, path: Union[str, Path], data: Any) -> None:
        """Optimized write with memory mapping for large data"""
        if isinstance(data, str):
            binary_data = data.encode('utf-8')
        elif isinstance(data, bytes):
            binary_data = data
        else:
            binary_data = pickle.dumps(data)

        with open(path, 'wb') as f:
            f.write(b'\0' * len(binary_data))
            f.flush()
            with mmap.mmap(f.fileno(), len(binary_data), access=mmap.ACCESS_WRITE) as mm:
                mm.write(binary_data)
                mm.flush()
