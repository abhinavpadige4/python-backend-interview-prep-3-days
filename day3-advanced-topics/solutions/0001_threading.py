"""
Threading and Concurrency Solution

Concurrency concepts and implementations for backend interview preparation.
Covers:
- Threading basics and thread safety
- Locks, RLocks, Semaphores
- Thread pools and executors
- Queue implementations
- GIL implications
- Multiprocessing vs threading
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Any
import multiprocessing as mp

# Thread Safety Examples
THREAD_SAFETY_EXAMPLES = '''
# Unsafe Counter (Race Condition)
class UnsafeCounter:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        # Race condition: read-modify-write is not atomic
        self.count += 1

# Safe Counter with Lock
class SafeCounter:
    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()
    
    def increment(self):
        with self._lock:
            self.count += 1
    
    def get_count(self):
        with self._lock:
            return self.count

# Safe Counter with RLock (Reentrant Lock)
class ReentrantCounter:
    def __init__(self):
        self.count = 0
        self._lock = threading.RLock()  # Allows same thread to acquire multiple times
    
    def increment(self):
        with self._lock:
            self.count += 1
    
    def increment_twice(self):
        with self._lock:
            self.count += 1
            self.count += 1  # Same thread can re-acquire RLock
    
    def get_count(self):
        with self._lock:
            return self.count
'''

# Producer-Consumer Pattern
PRODUCER_CONSUMER = '''
import threading
import queue
import time
import random

def producer(q, producer_id, num_items):
    """Producer function that puts items into the queue."""
    for i in range(num_items):
        item = f"Producer-{producer_id}-Item-{i}"
        q.put(item)
        print(f"Producer {producer_id} produced: {item}")
        time.sleep(random.uniform(0.1, 0.5))  # Simulate work
    
    # Put sentinel values to signal completion
    for _ in range(q.maxsize if hasattr(q, 'maxsize') else 10):
        q.put(None)  # None signals end of production

def consumer(q, consumer_id):
    """Consumer function that takes items from the queue."""
    while True:
        item = q.get()
        if item is None:  # Sentinel value to stop
            q.put(None)  # Put it back for other consumers
            break
        print(f"Consumer {consumer_id} consumed: {item}")
        time.sleep(random.uniform(0.2, 0.6))  # Simulate work
        q.task_done()  # Signal that task is completed

def producer_consumer_example():
    """Example of producer-consumer pattern."""
    # Create a queue with max size
    q = queue.Queue(maxsize=5)
    
    # Create producer and consumer threads
    producers = [
        threading.Thread(target=producer, args=(q, i, 3)) 
        for i in range(2)
    ]
    consumers = [
        threading.Thread(target=consumer, args=(q, i)) 
        for i in range(3)
    ]
    
    # Start all threads
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    
    # Wait for producers to finish
    for p in producers:
        p.join()
    
    # Wait for queue to be empty and consumers to finish
    q.join()
    
    # Signal consumers to exit by putting None values
    for _ in consumers:
        q.put(None)
    
    # Wait for consumers to finish
    for c in consumers:
        c.join()
    
    print("Producer-consumer example completed.")
'''

# Thread Pool Examples
THREAD_POOL_EXAMPLES = '''
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def worker_task(task_id, duration):
    """Simulate a worker task."""
    print(f"Task {task_id} starting...")
    time.sleep(duration)
    result = f"Task {task_id} completed after {duration:.2f}s"
    print(result)
    return result

def thread_pool_example():
    """Example using ThreadPoolExecutor."""
    print("Starting thread pool example...")
    
    # Method 1: Using map (simple case)
    with ThreadPoolExecutor(max_workers=3) as executor:
        durations = [1, 2, 1, 3, 2]
        results = list(executor.map(worker_task, range(5), durations))
        print("Map results:", results)
    
    print("\n" + "-"*40 + "\n")
    
    # Method 2: Using submit and as_completed (more control)
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        futures = [
            executor.submit(worker_task, i, random.uniform(0.5, 2.0))
            for i in range(5)
        ]
        
        # Process results as they complete
        results = []
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Got result: {result}")
    
    print("Thread pool example completed.")
'''

# Process Pool Example (for CPU-bound tasks)
PROCESS_POOL_EXAMPLES = '''
import math
from concurrent.futures import ProcessPoolExecutor

def is_prime(n):
    """CPU-intensive task: check if number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def find_primes_in_range(start, end):
    """Find all prime numbers in a range."""
    primes = []
    for num in range(start, end):
        if is_prime(num):
            primes.append(num)
    return primes

def process_pool_example():
    """Example using ProcessPoolExecutor for CPU-bound tasks."""
    print("Starting process pool example...")
    
    # Define ranges to check for primes
    ranges = [
        (1, 1000),
        (1000, 2000),
        (2000, 3000),
        (3000, 4000),
        (4000, 5000)
    ]
    
    with ProcessPoolExecutor(max_workers=3) as executor:
        # Submit all ranges
        futures = [
            executor.submit(find_primes_in_range, start, end)
            for start, end in ranges
        ]
        
        # Collect results
        all_primes = []
        for future in futures:
            primes = future.result()
            all_primes.extend(primes)
            print(f"Found {len(primes)} primes in range")
    
    print(f"Total primes found: {len(all_primes)}")
    print(f"First 10 primes: {all_primes[:10]}")
    print("Process pool example completed.")
'''

# Thread Local Storage
THREAD_LOCAL_EXAMPLES = '''
import threading

# Thread-local storage example
local_data = threading.local()

def worker_with_thread_local(worker_id):
    """Worker function using thread-local storage."""
    # Each thread gets its own copy of local_data
    local_data.worker_id = worker_id
    local_data.counter = 0
    
    # Simulate some work
    for i in range(5):
        local_data.counter += 1
        print(f"Worker {local_data.worker_id}: counter = {local_data.counter}")
        time.sleep(0.1)
    
    print(f"Worker {local_data.worker_id} final counter: {local_data.counter}")

def thread_local_example():
    """Example demonstrating thread-local storage."""
    print("Starting thread-local storage example...")
    
    threads = [
        threading.Thread(target=worker_with_thread_local, args=(i,))
        for i in range(3)
    ]
    
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    print("Thread-local storage example completed.")
'''

# Lock Types Comparison
LOCK_TYPES = '''
Lock Types in Python threading:

1. Lock (primitive lock)
   - Basic mutual exclusion lock
   - Can be acquired and released
   - Attempting to acquire twice by same thread blocks

2. RLock (Reentrant Lock)
   - Can be acquired multiple times by same thread
   - Must be released same number of times acquired
   - Useful for recursive algorithms

3. Semaphore
   - Controls access to a resource with limited capacity
   - Internal counter decremented on acquire, incremented on release
   - Useful for limiting concurrent access (e.g., database connection pool)

4. BoundedSemaphore
   - Like Semaphore but prevents exceeding initial value
   - Raises ValueError if released more times than acquired

5. Condition
   - Allows threads to wait for certain conditions
   - Combines lock with wait/notify mechanism
   - Useful for producer-consumer patterns

6. Event
   - Simple signaling mechanism between threads
   - Threads can wait for event to be set
   - Useful for simple coordination

7. Barrier
   - Synchronizes fixed number of threads
   - All threads must reach barrier before any can proceed
   - Useful for parallel phases in computation
'''

# GIL Explanation
GIL_EXPLANATION = '''
Global Interpreter Lock (GIL) Explanation:

What is the GIL?
- Mutex that protects access to Python objects
- Prevents multiple native threads from executing Python bytecodes simultaneously
- Ensures thread safety for Python's memory management

Impact on Concurrency:
- CPU-bound threads: Limited by GIL, true parallelism not achieved
- I/O-bound threads: Can benefit from threading (GIL released during I/O)
- Multiprocessing: Bypasses GIL entirely (separate Python interpreters)

When to Use Threading vs Multiprocessing:
- Use Threading for:
    - I/O-bound tasks (network requests, file operations, database queries)
    - When you need shared memory space
    - Simple concurrent operations
    
- Use Multiprocessing for:
    - CPU-bound tasks (mathematical computations, data processing)
    - When you need true parallelism
    - When GIL becomes a bottleneck
    - Tasks that can be easily parallelized

Hybrid Approaches:
- Use threading for I/O, multiprocessing for CPU-intensive parts
- Consider asyncio for high-concurrency I/O scenarios
'''

def print_threading_examples():
    """Print threading and concurrency examples for reference."""
    print("=== THREAD SAFETY EXAMPLES ===")
    print(THREAD_SAFETY_EXAMPLES.strip())
    print("\n=== PRODUCER-CONSUMER PATTERN ===")
    print(PRODUCER_CONSUMER.strip())
    print("\n=== THREAD POOL EXAMPLES ===")
    print(THREAD_POOL_EXAMPLES.strip())
    print("\n=== PROCESS POOL EXAMPLES ===")
    print(PROCESS_POOL_EXAMPLES.strip())
    print("\n=== THREAD LOCAL STORAGE ===")
    print(THREAD_LOCAL_EXAMPLES.strip())
    print("\n=== LOCK TYPES ===")
    print(LOCK_TYPES.strip())
    print("\n=== GIL EXPLANATION ===")
    print(GIL_EXPLANATION.strip())

if __name__ == "__main__":
    print_threading_examples()
    
    # Concurrency Interview Tips
    print("\n" + "="*50)
    print("CONCURRENCY INTERVIEW TIPS:")
    print("="*50)
    print("1. Understand the difference between parallelism and concurrency")
    print("2. Know when to use threading vs multiprocessing vs asyncio")
    print("3. Understand the GIL and its implications")
    print("4. Be able to implement thread-safe data structures")
    print("5. Know different synchronization primitives (Lock, Semaphore, etc.)")
    print("6. Understand producer-consumer patterns and queues")
    print("7. Be familiar with thread pools and executors")
    print("8. Know how to handle shared state safely")
    print("9. Understand deadlock conditions and how to prevent them")
    print("10. Practice explaining race conditions and solutions")
    print("11. Know when to use thread-local storage")
    print("12. Understand the performance characteristics of each approach")