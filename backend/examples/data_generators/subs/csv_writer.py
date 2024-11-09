import csv
import os
import io
from typing import List, Dict, Any, Union
from pathlib import Path

def standard_csv_writer(data: List[Dict[str, Any]], filename: Union[str, Path]) -> None:
    """Writes CSV file using the standard csv.DictWriter."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def low_level_writer(data: List[Dict[str, Any]], filename: Union[str, Path]) -> None:
    """Optimized low-level writer using binary mode and proper buffering."""
    fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o666)
    try:
        with os.fdopen(fd, 'wb', buffering=8192) as file:
            writer = csv.writer(io.TextIOWrapper(file, encoding='utf-8'))
            writer.writerow(data[0].keys())
            for row in data:
                writer.writerow(row.values())
    except Exception as e:
        os.close(fd)
        raise e

def buffered_io_writer(data: List[Dict[str, Any]], filename: Union[str, Path], buffer_size: int = 8192) -> None:
    """Enhanced buffered writer with configurable buffer size."""
    with open('backend/examples/common/file_headers/person.csv', 'r') as header_file:
        header = next(csv.reader(header_file))    
    with io.open(filename, mode='w', buffering=buffer_size, encoding='utf-8') as file:
        file.write(','.join(header) + '\n')
        for row in data:
            file.write(','.join(str(value) for value in row.values()) + '\n')

def chunked_writer(data: List[Dict[str, Any]], filename: Union[str, Path], chunk_size: int = 5000) -> None:
    """Memory-efficient chunked writer with configurable chunk size."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        
        for i in range(0, len(data), chunk_size):
            chunk = data[i:i + chunk_size]
            writer.writerows(chunk)