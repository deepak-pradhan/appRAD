"""
Create Sample Files Generator

Creates a variety of sample files in different sizes and formats for testing and demonstration.
Files are stored in a persistent data directory for reference and benchmarking.

Usage:
    python -m backend.examples.file_management.create_file_samples
"""

from backend.models.bases.filesystem_base import FileSystemBase
from backend.models.bases.file_handler_base import FileHandlerBase
from pathlib import Path
import random
import string
import time
from enum import Enum
import json
import os

class FileType(Enum):
    TEXT = "Text and Document Files"
    EBCDIC = "Text Files"
    BINARY = "Binary Files"
    JSON = "JSON Files"
    CSV = "CSV Files"
    XML = "XML Files"
    YAML = "YAML Files"
    
class FileSizeCategory_Legacy(Enum):
    # Typical legacy medias
    FLOPPY = (1_440 * 1_024, "1.44 MB")
    CD = (700 * 1024 * 1024, "700 MB")
    DVD = (4.38 * 1024 * 1024 * 1024, "4.38 /4.7 GB")
    DVD_PLUS = (7.92 * 1024 * 1024 * 1024, "7.92 /8.5 GB")
    BLU_RAY = (25 * 1024 * 1024 * 1024, "25 GB")
    BLU_RAY_PLUS = (50 * 1024 * 1024 * 1024, "50 GB")

class FileSizeCategory_System(Enum):
    # Typical RC & PIDs.
    RC = (1, "1 bytes") # 1 byte, return code
    PID_16 = (5, "5 bytes") # process ID for 16-bit systems
    PID_32 = (7, "7 bytes") # process ID for 32-bit & 64 bits systems, max = 4194303    
    
class FileSizeCategory_Configs(Enum):
    # Typical CONFIG files 10 bytes to 100 KB
    # Generally preferences in/ for  : .ini, .env, .xml, .json, .yaml, system alerts & notifications, ...
    CFG_TINY = (50, "50 bytes")
    CFG_TINY_MINY = (100, "100 byes")
    CFG_TINY_SMALL = (500, "500 bytes")
    CFG_MINI = (1024, "1 KB")
    CFG_SMALL = (5 * 1024, "5 KB")
    CFG_MEDIUM = (10 * 1024, "10 KB")
    #(nginx.conf, httpd.conf) or large .json configs used by complex applications.
    CFG_LARGE = (100 * 1024, "50 KB") 
    CFG_LARGER = (100 * 1024, "100 KB") 
    CFG_LARGEST = (500 * 1024 * 1024, "500 KB")

class FileSizeCategory_Logs(Enum):
    # Typical LOG files 100 KB to 10 MB
    # Generally logs, error logs, access logs, system logs, audit logs, etc.
    LOG_TINY = (100 * 1024, "100 KB")
    LOG_MINI = (500 * 1024, "500 KB")
    LOG_SMALL = (1024 * 1024, "1 MB")
    LOG_MEDIUM = (5 * 1024 * 1024, "5 MB")
    LOG_LARGE = (10 * 1024 * 1024, "10 MB")

class FileSizeCategory_Text(Enum):
    # Typical ascii TEXT files 10 MB to 5 GB
    # Generally text files, data files, reports, csv, txt, log, etc.
    # 25, 50, 100. 500 MB. 1, 5. 10
    TEXT_FLOPPY = (int(1_440 * 1_024), "1.44 MB")
    TEXT_TINY = (int(10 * 1024 * 1024), "10 MB")
    TEXT_MINI = (int(50 * 1024 * 1024), "50 MB")
    TEXT_SMALL = (int(100 * 1024 * 1024), "100 MB")
    TEXT_MEDIUM = (int(500 * 1024 * 1024), "500 MB")
    TEXT_CD = (int(700 * 1024 * 1024), "700 MB")
    TEXT_LARGE = (int(1000 * 1024 * 1024), "1 GB")
    TEXT_DVD = (int(4.38 * 1024 * 1024 * 1024), "4.38 /4.7 GB")
    TEXT_DVD_PLUS = (int(7.92 * 1024 * 1024 * 1024), "7.92 /8.5 GB")
    TEXT_BLU_RAY = (int(25 * 1024 * 1024 * 1024), "25 GB")
    TEXT_BLU_RAY_PLUS = (int(50 * 1024 * 1024 * 1024), "50 GB")

class FileTypeCategory(Enum):
    # Documents: DOCX, PDF, PPTX, XLSX, RTF, ODT
    # Data: CSV, JSON, XML, XSD, Parquet, Avro, 
    # Images: JPG, PNG
    # Audio MP3, WAV    
    # Video MP4, AVI, MOV
    pass

     
def generate_metadata(file_type, size):
    return {
        "created_at": time.time(),
        "file_type": file_type.value,
        "size": size,
        "checksum": "sha256_hash_here"
    }

def create_text_file(data_dir):
    data_dir.mkdir(parents=True, exist_ok=True)
    
    fs = FileSystemBase(data_dir)
    fh = FileHandlerBase()    

    print(f"Output directory: {data_dir}\n")
   
    # Create samples for each file type and size
    # @TODO: create content = noises(randomly generated)
    # @TODO: create log time elapsed
    # @TODO: write file mt

    print(f"\nCreating Text files:")
    total_files = len(FileSizeCategory_Text)
    for idx, size_cat in enumerate(FileSizeCategory_Text, 1):
        size, size_label = size_cat.value
        print(f"  Creating {size_label} file...")
            
        start_time = time.time()
           
        content = ''.join(random.choices(string.ascii_letters + string.digits + ' \n', k=size))
        filename = f"sample_text_{size_label.replace(' ','_')}.txt"
        fh.write_text(data_dir / filename, content)
                
        
        elapsed = time.time() - start_time
        print(f"    Created {filename} in {elapsed:.4f} seconds")
        print(f"Progress: {idx}/{total_files} files created")           
    

if __name__ == "__main__":
    data_dir = Path("backend/examples/file_management/external/ins/5.stages")
    create_text_file(data_dir)

