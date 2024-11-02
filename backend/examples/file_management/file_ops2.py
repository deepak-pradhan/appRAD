"""
File Operations Demo Module

This module demonstrates efficient file operations using FileSystemBase and FileHandlerBase.
It creates sample files in a persistent data directory for reference and testing purposes.

Key Features:
- Creates binary test files with configurable sizes
- Measures write performance
- Generates sample JSON configuration
- Demonstrates file read/write operations

Usage:
    python -m backend.examples.file_management.file_ops2

Example Output:
    Working directory: /path/to/backend/examples/file_management/data
    Created: /path/to/data/standard_0.bin
    ...
    Created sample config: /path/to/data/config.json
    Read config successfully: {'app_name': 'FileOps Demo', ...}

The sample files remain available in the data directory for further examination.
"""

# Imports
from backend.models.bases.filesystem_base import FileSystemBase
from backend.models.bases.file_handler_base import FileHandlerBase
from pathlib import Path
import time

def demo_file_operations():
    """
    Demonstrates file system operations by creating sample files and measuring performance.
    
    Creates:
    - Binary files with 100KB test data
    - JSON configuration file with sample settings
    - Performance metrics for write operations
    
    Returns:
        None
    """
    '''
    To test and measure time for the methods in file_handler_base.py  we will use file_ops2.py. 

    To test read methods
    1. Create raw but meaninf full text samples files in backend/examples/file_management/data/
        text_very_small.txt
        text_file_small.txt
        text_file_medium.txt
        text_file_large.txt
        text_file_very_large.txt

    2. Create CSV samples files in backend/examples/file_management/data/
        csv_very_small.csv
        csv_file_small.csv
        csv_file_medium.csv
        csv_file_large.csv

    3. Create structured json samples files in backend/examples/file_management/data/
        json_very_small.json
        json_file_small.json
        json_file_medium.json
        json_file_large.json


    4. Create EBCDIC samples files in backend/examples/file_management/data/
        ebc_very_small.cbl
        ebc_file_small.cbl
        ebc_file_medium.cbl
        ebc_file_large.cbl

    5. Create structured RDF/XML samples files in backend/examples/file_management/data/
        rdf_xml_very_small.xml
        rdf_xml_file_small.xml
        rdf_xml_file_medium.xml
        rdf_xml_file_large.xml
        
    6. Create structured RDF/JSON-LD samples files in backend/examples/file_management/data/
        rdf_ld_very_small.json
        rdf_ld_file_small.json
        rdf_ld_file_medium.json
        rdf_ld_file_large.json

    7. Create structured parquet samples files in backend/examples/file_management/data/
        par_very_small.parquet
        par_file_small.parquet
        par_file_medium.parquet
        par_file_large.parquet

    8. Create structured pickle samples files in backend/examples/file_management/data/
        pic_ld_very_small.rdfl
        pic_ld_file_small.cbl
        pic_ld_file_medium.cbl
        pic_ld_file_large.cbl

    Similarly, list what samples for other file types such as binary, text, etc.


            To test write_text()
    Read the data/text_*.text files and create a config.json file in data

    To test read_binary()
    '''
    # Create a permanent data directory for samples
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    fs = FileSystemBase(data_dir)
    fh = FileHandlerBase()
    
    test_data = b"x" * 100_000  # 100KB of data
    iterations = 5
    
    print(f"\nWorking directory: {data_dir}")
    
    # Test standard write
    start_time = time.time()
    for i in range(iterations):
        file_path = fs.root / f"standard_{i}.bin"
        fh.write_binary(file_path, test_data)
        print(f"Created: {file_path}")
        
    standard_time = time.time() - start_time
    
    # Create some sample JSON data
    sample_config = {
        "app_name": "FileOps Demo",
        "version": "1.0",
        "settings": {
            "max_file_size": 1024000,
            "compression": True
        }
    }
    
    config_path = fs.root / "config.json"
    fh.write_json(config_path, sample_config)
    print(f"\nCreated sample config: {config_path}")
    
    # Read and display the config
    loaded_config = fh.read_json(config_path)
    print(f"Read config successfully: {loaded_config}")
    
    print(f"\nAll sample files are available in: {data_dir}")

if __name__ == "__main__":
    demo_file_operations()