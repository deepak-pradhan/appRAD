from backend.models.bases.filesystem_base import FileSystemBase
from backend.models.bases.file_handler_base import FileHandlerBase
from pathlib import Path
import time

'''
Usage:
python -m backend.examples.file_management.file_ops
'''
def demo_file_operations():
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