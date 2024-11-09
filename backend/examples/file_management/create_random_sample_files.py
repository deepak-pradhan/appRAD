"""
High Performance Sample Files Generator

Creates optimized sample files using low-level system calls and memory mapping.
Supports multi-processing for large file generation with progress tracking.

Usage:
    cd appRAD/sbox1
    python -m backend.examples.file_management.create_random_sample_files
"""

import os
import sys
import random
import string
import psutil
import multiprocessing as mp # supports both local and remote concurrency,
import threading

from pathlib import Path
from enum import Enum
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
from typing import Union

from backend.models.bases.filesystem_base import FileSystemBase
from backend.models.bases.file_handler_base import FileHandlerBase

# Dictionary to switch write behavior
WRITE_BEHAVIOR = {
    "overwrite": "w",
    "append": "a",
    "truncate": "w",
}

class FileType(Enum):
    TEXT = ("Text Files", '.txt')
    EBCDIC = ("EBCDIC Files", '.ebcdic')
    BINARY = ("Binary Files", '.bin')


class FileSizeCategory_Text(Enum):
    '''
    @TODO: Larger than XXX bytes, use mmap to map the file into memory
    '''
    TEXT_ALERT = (int(50), "50 Bytes")    
    TEXT_MESSAGE = (int(50), "100 Bytes")    
    TEXT_500B = (int(500), "500 Bytes")
    TEXT_1KB = (int(1024), "1 KB")
    TEXT_5KB = (int(5 * 1024), "5 KB")
    TEXT_10KB = (int(10 * 1024), "10 KB")
    TEXT_50KB = (int(100 * 1024), "50 KB") 
    TEXT_100KB = (int(100 * 1024), "100 KB") 
    TEXT_500KB = (int(500 * 1024 * 1024), "500 KB")
    TEXT_1MB = (int(1024 * 1024), "1 MB")
    TEXT_FLOPPY = (int(1_440 * 1_024), "Floppy")
    TEXT_10MB = (int(10 * 1024 * 1024), "10 MB")
    TEXT_50MB = (int(50 * 1024 * 1024), "50 MB")
    TEXT_CHUNK = (int(100 * 1024 * 1024), "100 MB")
    # TEXT_500MB = (int(500 * 1024 * 1024), "500 MB")
    # TEXT_CD = (int(700 * 1024 * 1024), "700 MB")
    # TEXT_1GB = (int(1 * 1024 * 1024 * 1024), "1 GB")
    # TEXT_5GB = (int(5 * 1024 * 1024 * 1024), "5 GB")
     

def get_ascii(size: int) -> str:
    chunk_size = min(size, 100 * 1024 * 1024)  
    content = []  # List to accumulate chunks efficiently
    for offset in range(0, size, chunk_size):
        current_chunk = min(chunk_size, size - offset)
        ascii_text = ''.join(random.choices(string.ascii_letters + string.digits + ' \n', k=current_chunk))
        content.append(ascii_text)
    return ''.join(content)

def get_binary(size: int) -> bytes:
    chunk_size = min(size, 100 * 1024 * 1024)
    binary_content = bytearray()
    for offset in range(0, size, chunk_size):
        current_chunk = min(chunk_size, size - offset)
        binary_content.extend(os.urandom(current_chunk))
    return bytes(binary_content) 

def get_ebcdic(size: int) -> bytes:
    chunk_size = min(size, 100 * 1024 * 1024) 
    ebcdic_content = bytearray() 
    for offset in range(0, size, chunk_size):
        current_chunk = min(chunk_size, size - offset)
        ascii_text = ''.join(random.choices(string.ascii_letters + string.digits + ' \n', k=current_chunk))
        ebcdic_content.extend(ascii_text.encode('cp500'))
    return bytes(ebcdic_content)  # Return as immutable bytes

def write_file(filepath: Path, content: Union[str, bytes]) -> None:
    # Determine mode based on content type
    mode = 'wb' if isinstance(content, bytes) else 'w'    
    with open(filepath, mode) as f:
        f.write(content)
    return 1

def write_chunks(filepath: Path, content: Union[str, bytes], chunk_size: int = 100 * 1024 * 1024) -> None:
    mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(filepath, mode) as f:
        for i in range(0, len(content), chunk_size):
            chunk = content[i:i + chunk_size]
            f.write(chunk)
            f.flush()  # Flush to disk to manage memory efficiently
    return 1

def x_write_binary_data(filepath: Path, content: Union[str, bytes]):
    with os.fdopen(os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_BINARY), 'wb') as file:
        file.write(content)
def x_write_ascii_data(filepath: Path, content: Union[str, bytes]):
    with os.fdopen(os.open(filepath, os.O_WRONLY | os.O_CREAT | os.O_TEXT), 'w') as file:
        file.write(content)
def x_write_ebcdic_data(filepath: Path, content: Union[str, bytes]):
    x_write_binary_data(filepath, content)
def display_elapsed_time(start_time: datetime, end_time: datetime) -> str:
    elapsed = end_time - start_time    
    hours, remainder = divmod(elapsed.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    microseconds = elapsed.microseconds
    return f"{int(hours):02}.{int(minutes):02}.{int(seconds):02}.{microseconds:06}"

def format_byte_size(byte_size):
    for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
        if byte_size < 1024:
            return f"{byte_size} {unit}"
        byte_size /= 1024
    return f"{byte_size} PB"  # For extremely large sizes

def get_content (bytes: int, encoding_type: str):
    match encoding_type.lower():
        case "ascii":
            process_id = os.getpid()
            thread_id = threading.get_ident()
            start_time = datetime.now()
            content = get_ascii(bytes)
            end_time = datetime.now()
            print(f"PID: {process_id}, TID: {thread_id}, Created {format_byte_size(bytes)} ascii in {display_elapsed_time(start_time, end_time)}")
            return content

        case "binary":
            process_id = os.getpid()
            thread_id = threading.get_ident()
            start_time = datetime.now()
            content = get_binary(bytes)
            end_time = datetime.now()
            print(f"PID: {process_id}, TID: {thread_id}, Created {format_byte_size(bytes)} binary in {display_elapsed_time(start_time, end_time)}")
            return content

        case "ebcdic":
            process_id = os.getpid()
            thread_id = threading.get_ident()
            start_time = datetime.now()
            content = get_ebcdic(bytes)
            end_time = datetime.now()
            print(f"PID: {process_id}, TID: {thread_id}, Created {format_byte_size(bytes)} in {display_elapsed_time(start_time, end_time)}")
            return content

        case _:
            raise ValueError("Unsupported encoding type. Choose from 'ascii', 'binary', or 'ebcdic'.")

def write_file_fn (filepath : str, encoding_type: str, bytes_size: int, content: str):
    match encoding_type.lower():
        case "ascii":
            
            process_id = os.getpid()
            thread_id = threading.get_ident()
            start_time = datetime.now()
            if bytes_size < 100 * 1024 * 1024:
                is_pass = write_file(filepath, content)
            else:
                is_pass = write_chunks(filepath, content)
            end_time = datetime.now()
            print(f"PID: {process_id}, TID: {thread_id}, Wrote {format_byte_size(bytes_size)} ascii in {display_elapsed_time(start_time, end_time)}")

            # process_id = os.getpid()
            # thread_id = threading.get_ident()
            # start_time = datetime.now()
            # @NOTE: Faied to write 100MB+ files
            # is_pass = x_write_ascii_data(filepath, content)
            # end_time = datetime.now()
            # print(f"PID: {process_id}, TID: {thread_id}, x_Wrote {bytes_size} ascii bytes in {display_elapsed_time(start_time, end_time)}")

            return is_pass

        case "binary":
            process_id = os.getpid()
            thread_id = threading.get_ident()
            start_time = datetime.now()
            if bytes_size < 100 * 1024 * 1024:
                is_pass = write_file(filepath, content)
            else:
                is_pass = write_chunks(filepath, content)
            end_time = datetime.now()
            print(f"PID: {process_id}, TID: {thread_id}, Wrote {format_byte_size(bytes_size)} binary in {display_elapsed_time(start_time, end_time)}")

            # process_id = os.getpid()
            # thread_id = threading.get_ident()
            # start_time = datetime.now()
            # is_pass = x_write_binary_data(filepath, content)
            # end_time = datetime.now()
            # print(f"PID: {process_id}, TID: {thread_id}, x_Wrote {bytes_size} binary bytes in {display_elapsed_time(start_time, end_time)}")

            return is_pass

        case "ebcdic":
            pass

        case _:
            raise ValueError("Unsupported encoding type. Choose from 'ascii', 'binary', or 'ebcdic'.")
        
def process_file_creation(args):
    byte_size, label, data_dir = args
    filename_ascii  = f"sample_text_{label.replace(' ','_')}.txt"
    filename_binary = f"sample_text_{label.replace(' ','_')}.bin"
    filename_ebcdic = f"sample_text_{label.replace(' ','_')}.ascii"

    filepath_ascii = data_dir / filename_ascii
    filepath_binary = data_dir / filename_binary
    filepath_ebcdic = data_dir / filename_ebcdic

    # print(f">> Starting {size_label} ({size} bytes)")
    content_ascii  = get_content(byte_size, 'ascii')
    content_binary = get_content(byte_size, 'binary')
    content_ebcdic = get_content(byte_size, 'ebcdic')

    write_file_fn(filepath_ascii, 'ascii', byte_size, content_ascii)
    write_file_fn(filepath_binary, 'binary', byte_size, content_binary)
    write_file_fn(filepath_ebcdic, 'ebcdic', byte_size, content_ebcdic)


    start_time = datetime.now()
    end_time = datetime.now()
    elapsed = end_time - start_time    
    return filename_ascii, elapsed  


def create_random_files(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)    
    
    # Prepare work from Enum items
    work_items = [(item.value[0], item.value[1], data_dir) 
        for item in FileSizeCategory_Text]
    
    # Batch size for ProcessPoolExecutor
    # executor = ThreadPoolExecutor(max_workers=3)
    with ProcessPoolExecutor() as executor:
        total = len(work_items)
        for idx, (filename, elapsed) in enumerate(executor.map(process_file_creation, work_items), 1):
            print(f"\nProgress: {idx}/{total} files created")
            print(f"Created {filename} in {elapsed}")

if __name__ == "__main__":
    data_dir = Path("backend/examples/file_management/external/src1/noises")

    print(f"CPU cores available: {mp.cpu_count()}")
    print(f"Memory usage: {psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB")
    print(f"Output directory: {data_dir} \n")

    create_random_files(data_dir)

