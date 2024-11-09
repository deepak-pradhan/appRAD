import io
import csv
from typing import List, Dict, Any, Union
from pathlib import Path

DIR_FILE_HEADER = 'backend/examples/common/schemas'

def _get_header(schema: str) -> None:
    HEADER = f"{DIR_FILE_HEADER}/{schema}.csv" 
    with open(HEADER, 'r') as header_file:
        header = next(csv.reader(header_file))
    return header
    
def write(schema: str, data: List[Dict[str, Any]], filename: Union[str, Path], buffer_size: int = 8192) -> None:
    header = _get_header(schema)    
    with io.open(filename, mode='w', buffering=buffer_size, encoding='utf-8') as file:
        file.write(','.join(header) + '\n')
        for row in data:
            file.write(','.join(str(value) for value in row.values()) + '\n')
