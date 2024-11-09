from enum import Enum
import os
import psutil
from time import perf_counter  # More precise than time()
import multiprocessing as mp # supports both local and remote concurrency,
from backend.examples.data_generators.subs.generator_people import generate_data
from backend.examples.data_generators.subs.csv_writer import standard_csv_writer, low_level_writer, buffered_io_writer, chunked_writer

class FileSizes(Enum):
    '''
    Predefined file sizes to be generated
    , as friendly names = (label, byte size values).
    '''
    TINY_1KB = ("1 KB", 1 * 1024)
    TINY_4KB = ("4 KB", 4 * 1024)
    TINY_8KB = ("8 KB", 8 * 1024)
    TINY_16KB = ("16 KB", 16 * 1024)
    TINY_32KB = ("32 KB", 32 * 1024)
    TINY_64KB = ("64 KB", 64 * 1024)
    TINY_128KB = ("128 KB", 128 * 1024)
    TINY_512KB = ("512 KB", 512 * 1024)
    FLOPPY = ("1.44 MB", 1_440 * 1024)
    MINI_16MB = ("16 MB", 16 * 1024 * 1024)
    MINI_32MB = ("32 MB", 32 * 1024 * 1024)
    MINI_64MB = ("64 MB", 64 * 1024 * 1024)
    MINI_128MB = ("128 MB", 128 * 1024 * 1024)
    MINI_512MB = ("512 MB", 512 * 1024 * 1024)
    CD = ("700 MB", 700 * 1024 * 1024)
    DVD = ("4.38 GB / 4.7 GB", int(4.38 * 1024 * 1024 * 1024))

import threading

def format_time(seconds):
    """Format time in minutes and seconds if over 60 seconds"""
    if seconds >= 60:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.6f}s"
    return f"{seconds:.6f}s"

def benchmark_writer(writer_func, data, filename, name):
    pid = os.getpid()
    process_pid = psutil.Process(pid)
    
    # Get initial CPU and memory stats
    kb = float(1024)
    mb = float(kb ** 2)
    gb = float(kb ** 3)

    start_memory = int(psutil.virtual_memory().available/gb)
   
    thread_id = threading.current_thread().ident
    
    start_time = perf_counter()
    
    # Run writer function
    writer_func(data, filename)
    
    end_time = perf_counter()
    end_memory = int(psutil.virtual_memory().available/gb)
    elapsed_time = end_time - start_time
    memory_used = end_memory - start_memory
    
    cpu_percent = psutil.cpu_percent(interval=1.0)
    
    print(f"{name}, {writer_func.__name__}, {process_pid}, {thread_id}, {cpu_percent:.2f}, {start_memory}, {end_memory}, {memory_used:.4f} MB, {format_time(elapsed_time)}")

# Example Usage
if __name__ == "__main__":

    print(f"CPU cores available: {mp.cpu_count()}")
    print(f"Memory total: {psutil.virtual_memory()[0]/(1024 * 1024 * 1024)} GB")
    print(f"Memory usage: {psutil.virtual_memory().used }")

    print(f"Name, Writer, Process ID, Thread ID, CPU Usage, Start Mempry, End Memory, Memory Usage, Time Elapsed")

    for size_enum in FileSizes:
        size = size_enum.value[1]  # Access byte size from the Enum
        name = size_enum.name
        data = generate_data(size)
        # print(f"\n\n--- Benchmarking for Target Size: {size} bytes ---")
        benchmark_writer(standard_csv_writer, data, f"standard_{name}.csv", name)
        benchmark_writer(low_level_writer, data, f"lowlevel_{name}.csv", name)
        benchmark_writer(buffered_io_writer, data, f"buffered_{name}.csv", name)
        benchmark_writer(chunked_writer, data, f"chunked_{name}.csv", name)

