from enum import Enum


class FileTypes(Enum):
    CSV = 'jpg'
    PARQUET = 'png'
    JSON = 'gif'            

# Usage
def validate_file_type(file_type):
    return file_type.lower() in [ft.value for ft in FileTypes]