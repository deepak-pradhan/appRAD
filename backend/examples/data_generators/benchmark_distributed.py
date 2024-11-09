import psutil
from time import perf_counter
from pathlib import Path
from backend.examples.data_generators.subs.generator_people import generate_data
from backend.examples.Zzzz.csv_writer_distributed import (
    dask_csv_writer, dask_parquet_writer, spark_parquet_writer
)

def format_time(seconds: float) -> str:
    """Format time in minutes and seconds if over 60 seconds"""
    if seconds >= 60:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.6f}s"
    return f"{seconds:.6f}s"

def benchmark_distributed_writer(writer_func, data, filename):
    process = psutil.Process()
    process.cpu_percent()  # Initialize CPU monitoring
    
    start_memory = process.memory_info().rss / (1024 * 1024)
    start_time = perf_counter()
    
    writer_func(data, filename)
    
    end_time = perf_counter()
    end_memory = process.memory_info().rss / (1024 * 1024)
    
    elapsed_time = end_time - start_time
    memory_used = end_memory - start_memory
    cpu_percent = process.cpu_percent(interval=1.0)
    
    print(f"Distributed Writer: {writer_func.__name__}")
    print(f"CPU Usage: {cpu_percent:.2f}%")
    print(f"Memory Usage: {memory_used:.4f} MB")
    print(f"Time Elapsed: {format_time(elapsed_time)}\n")

if __name__ == "__main__":
    sizes = [1_000_000, 10_000_000, 100_000_000]  # Example sizes for large datasets
    
    for size in sizes:
        data = generate_data(size)
        print(f"\n--- Benchmarking Distributed Writers for {size:,} records ---")
        
        benchmark_distributed_writer(dask_csv_writer, data, f"dask_{size}.csv")
        benchmark_distributed_writer(dask_parquet_writer, data, f"dask_{size}.parquet")
        benchmark_distributed_writer(spark_parquet_writer, data, f"spark_{size}.parquet")
