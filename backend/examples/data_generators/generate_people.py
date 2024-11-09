from enum import Enum
from backend.examples.data_generators.subs.generator_people import generate_data
from backend.examples.utils.generate_schema_data import write

class FileSizes(Enum):
    '''
    Predefined file sizes with friendly names and byte size values.
    '''
    TINY_16KB = ("16 KB", 16 * 1024)
    MINI_16MB = ("16 MB", 16 * 1024 * 1024)
   

# Example Usage
if __name__ == "__main__":
    for size_enum in FileSizes:
        size = size_enum.value[1]  # Access byte size from the Enum
        name = size_enum.name
        data = generate_data(size)
        schema = 'person'
        write(schema, data, f"{name}.csv")

