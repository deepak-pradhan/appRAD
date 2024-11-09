'''
Create sample files in a persistent data directory for reference and testing purposes.
The sample files remain available in the data directory for further examination.

Usage:
    python -m backend.examples.create_file_samples

Example Output:
    Output directory: backend/examples/file_management/external/ins

    Creating: FileType = 'Text and Document Files', Extension = 'txt', Size = 100 bytes
    Created: backend/examples/file_management/external/ins/text_100_btyes.txt
    Time taken: 0.00000019073486328125 seconds
'''    


# 1.a function to create random plain text files
import random
import string

def create_random_text_file(file_path, size_in_bytes):
    """
    Create a random plain text file of the specified size.
    Args:
        file_path (str): Path to the file.
        size_in_bytes (int): Size of the file in bytes.
    """
    with open(file_path, 'w') as file:
        file.write(''.join(random.choices(string.ascii_letters + string.digits, k=size_in_bytes)))
        
# 1.b function to create random binary files
directory = 'backend/examples/file_management/external/ins'
create_random_text_file(f"{directory}/text_file_tiny.txt", 100) # 500 bytes
create_random_text_file('text_file_tiny_small.txt', 1024) # 5 KB
create_random_text_file('text_file_tiny_medium.txt', 10240) # 50 KB
create_random_text_file('text_file_tiny_large.txt', 102400) # 500 KB
create_random_text_file('text_file_tiny_very_large.txt', 1024000) # 1 MB

create_random_text_file('text_file_mini.txt', 5240000) # 5 MB
create_random_text_file('text_file_small.txt', 52400000) # 50 MB
create_random_text_file('text_file_medium.txt', 524000000) # 500 MB
create_random_text_file('text_file_large.txt', 5240000000) # 5 GB
create_random_text_file('text_file_very_large.txt', 52400000000) # 50 GB





# , `Binary Files`, `Spreadsheet Files`, `Presentation Files`, `Database Files`, `Audio Files`, `Video Files`, `Archives`, `Executable Files`, `Source Code Files`, `Configuration Files`, `Log Files`, `Backup Files`, `Temporary Files`, `System Files`, `Email Files`, `Web Files`, `Font Files`, `Image Files`, `3D Files`, `CAD Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `GIS Files`, `
