class FileSystem:
    """A wrapper class for handling multiple file systems"""

    _supported_file_types = {
        "adb": ["parquet"], # PyArrow
        "ddb": ["csv", "parquet", "json"], # DuckDB
        "tdb": ["json"], # TinyDB
        "ldb" : ["db", "sqlite"], # Local RDBMS
        "s3" : ["csv", "parquet"],
    }
        
    def __init__(self, fs_type="local"):
        self.fs_type = fs_type

    
    def read(self, path):
        """Read file content from the specified path"""
        if self.fs_type == "local":
            with open(path, 'r') as f:
                return f.read()
        elif self.fs_type == "s3":
            # Implement S3 read logic here
            pass
            
    def write(self, path, content):
        """Write content to the specified path"""
        if self.fs_type == "local":
            with open(path, 'w') as f:
                f.write(content)
        elif self.fs_type == "s3":
            # Implement S3 write logic here
            pass
            
    def exists(self, path):
        """Check if file exists at the specified path"""
        if self.fs_type == "local":
            import os
            return os.path.exists(path)
        elif self.fs_type == "s3":
            # Implement S3 exists logic here
            pass
            
    def delete(self, path):
        """Delete file at the specified path"""
        if self.fs_type == "local":
            import os
            if self.exists(path):
                os.remove(path)
        elif self.fs_type == "s3":
            # Implement S3 delete logic here
            pass