"""
AsyncIO Programming Solution

Asynchronous programming concepts and implementations for backend interview preparation.
Covers:
- AsyncIO basics and event loop
- Coroutines and tasks
- Async/await syntax
- Concurrent execution with gather and wait
- Async context managers and iterators
- Working with aiohttp for HTTP requests
- Error handling in async code
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Any
import json

# AsyncIO Basics
ASYNCIO_BASICS = '''
AsyncIO Basics:

Event Loop:
    - Core of AsyncIO that executes asynchronous tasks
    - Manages scheduling and execution of coroutines
    - One event loop per thread (by default)

Coroutines:
    - Functions defined with async def
    - Can be paused and resumed
    - Return coroutine objects when called (not executed immediately)

Tasks:
    - Wrapper around coroutines for scheduling
    - Allow concurrent execution of coroutines
    - Created with asyncio.create_task() or asyncio.ensure_future()

Await:
    - Keyword to pause coroutine execution until awaitable completes
    - Can await coroutines, tasks, futures

Creating and Running Coroutines:
    async def my_coroutine():
        await asyncio.sleep(1)
        return "Done"
    
    # Method 1: Using asyncio.run() (Python 3.7+)
    result = asyncio.run(my_coroutine())
    
    # Method 2: Manual event loop (older Python)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(my_coroutine())
'''

# Basic Async/Await Examples
BASIC_ASYNC_EXAMPLES = '''
import asyncio
import time

async def fetch_data(delay: int, data: str) -> str:
    """Simulate fetching data with delay."""
    print(f"Fetching {data}...")
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(f"Fetched {data} after {delay}s")
    return f"Data: {data}"

async def process_data(data: str) -> str:
    """Process fetched data."""
    print(f"Processing {data}...")
    await asyncio.sleep(0.5)  # Simulate processing time
    result = f"Processed: {data.upper()}"
    print(f"Processed {data}")
    return result

async def main_sequential():
    """Sequential execution example."""
    print("Starting sequential execution...")
    start_time = time.time()
    
    result1 = await fetch_data(2, "API1")
    result2 = await fetch_data(2, "API2")
    result3 = await fetch_data(2, "API3")
    
    end_time = time.time()
    print(f"Sequential execution took {end_time - start_time:.2f}s")
    return [result1, result2, result3]

async def main_concurrent():
    """Concurrent execution example."""
    print("Starting concurrent execution...")
    start_time = time.time()
    
    # Create tasks that run concurrently
    task1 = asyncio.create_task(fetch_data(2, "API1"))
    task2 = asyncio.create_task(fetch_data(2, "API2"))
    task3 = asyncio.create_task(fetch_data(2, "API3"))
    
    # Wait for all tasks to complete
    results = await asyncio.gather(task1, task2, task3)
    
    end_time = time.time()
    print(f"Concurrent execution took {end_time - start_time:.2f}s")
    return results

async def main_mixed():
    """Mixed sequential and concurrent execution."""
    print("Starting mixed execution...")
    start_time = time.time()
    
    # First, fetch data concurrently
    fetch_tasks = [
        asyncio.create_task(fetch_data(1, "SourceA")),
        asyncio.create_task(fetch_data(1, "SourceB")),
        asyncio.create_task(fetch_data(1, "SourceC"))
    ]
    fetch_results = await asyncio.gather(*fetch_tasks)
    
    # Then process results sequentially
    process_results = []
    for data in fetch_results:
        processed = await process_data(data)
        process_results.append(processed)
    
    end_time = time.time()
    print(f"Mixed execution took {end_time - start_time:.2f}s")
    return process_results
'''

# Async Context Managers
ASYNC_CONTEXT_MANAGERS = '''
import asyncio
import aiofiles  # For async file operations

class AsyncDatabaseConnection:
    """Example async context manager for database connection."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    async def __aenter__(self):
        """Async enter - establish connection."""
        print(f"Connecting to database: {self.connection_string}")
        # Simulate async connection establishment
        await asyncio.sleep(0.5)
        self.connection = f"Connection to {self.connection_string}"
        print("Database connected")
        return self.connection
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async exit - close connection."""
        print("Closing database connection...")
        # Simulate async connection closure
        await asyncio.sleep(0.2)
        self.connection = None
        print("Database connection closed")
        # Return False to propagate exceptions
        return False

# Usage example
async def database_operations():
    """Example using async context manager."""
    async with AsyncDatabaseConnection("postgresql://localhost/mydb") as conn:
        print(f"Performing operations with {conn}")
        await asyncio.sleep(0.3)  # Simulate DB operations
        return f"Operations completed on {conn}"

# Async file operations with aiofiles
async def async_file_operations():
    """Example of async file operations."""
    # Async write
    async with aiofiles.open('temp.txt', 'w') as f:
        await f.write('Hello, Async World!\n')
        await f.write('This file was written asynchronously.\n')
    
    # Async read
    async with aiofiles.open('temp.txt', 'r') as f:
        content = await f.read()
        print("File content:")
        print(content)
    
    return content
'''

# Async Iterators
ASYNC_ITERATORS = '''
import asyncio

class AsyncNumberGenerator:
    """Async iterator that generates numbers with delay."""
    
    def __init__(self, start: int, stop: int, delay: float = 0.1):
        self.start = start
        self.stop = stop
        self.delay = delay
        self.current = start
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        
        await asyncio.sleep(self.delay)
        value = self.current
        self.current += 1
        return value

# Usage example
async def async_iterator_example():
    """Example using async iterator."""
    print("Async number generation:")
    async for number in AsyncNumberGenerator(1, 6, 0.2):
        print(f"Generated: {number}")
    
    # Alternative: using list comprehension
    numbers = [num async for num in AsyncNumberGenerator(1, 4, 0.1)]
    print(f"Collected numbers: {numbers}")
    
    return list(AsyncNumberGenerator(1, 4, 0.1))
'''

# Working with aiohttp
AIOHTTP_EXAMPLES = '''
import aiohttp
import asyncio

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """Fetch a single URL and return JSON response."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    'url': url,
                    'status': response.status,
                    'data': data,
                    'error': None
                }
            else:
                return {
                    'url': url,
                    'status': response.status,
                    'data': None,
                    'error': f'HTTP {response.status}'
                }
    except Exception as e:
        return {
            'url': url,
            'status': None,
            'data': None,
            'error': str(e)
        }

async def fetch_multiple_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch multiple URLs concurrently."""
    # Create a single session for all requests (recommended)
    async with aiohttp.ClientSession() as session:
        # Create tasks for all URLs
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        
        # Wait for all requests to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions that occurred
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'url': urls[i],
                    'status': None,
                    'data': None,
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results

# Example usage
async def aiohttp_example():
    """Example of using aiohttp for concurrent HTTP requests."""
    urls = [
        'https://httpbin.org/get',
        'https://httpbin.org/user-agent',
        'https://httpbin.org/headers'
    ]
    
    print("Fetching multiple URLs concurrently...")
    start_time = time.time()
    
    results = await fetch_multiple_urls(urls)
    
    end_time = time.time()
    print(f"Fetched {len(urls)} URLs in {end_time - start_time:.2f}s")
    
    for result in results:
        if result['error']:
            print(f"❌ {result['url']}: {result['error']}")
        else:
            print(f"✅ {result['url']}: Status {result['status']}")
    
    return results
'''

# Error Handling in AsyncIO
ERROR_HANDLING = '''
Error Handling in AsyncIO:

1. Exception Propagation:
    - Exceptions in coroutines propagate normally
    - Use try/except blocks within async functions
    - gather() with return_exceptions=True to handle exceptions gracefully

2. Timeout Handling:
    - Use asyncio.wait_for() to set timeouts
    - Use asyncio.shield() to protect from cancellation

3. Cancellation:
    - Tasks can be cancelled with task.cancel()
    - Handle CancelledError in coroutines
    - Use asyncio.shield() for critical operations

Examples:
'''

ERROR_HANDLING_EXAMPLES = '''
import asyncio

async def risky_operation(duration: float, should_fail: bool = False) -> str:
    """Simulate an operation that might fail or timeout."""
    await asyncio.sleep(duration)
    if should_fail:
        raise ValueError(f"Operation failed after {duration}s")
    return f"Success after {duration}s"

async def error_handling_examples():
    """Examples of error handling in AsyncIO."""
    
    # Example 1: Basic try/except
    print("Example 1: Basic exception handling")
    try:
        result = await risky_operation(1, should_fail=True)
    except ValueError as e:
        print(f"Caught exception: {e}")
    
    # Example 2: gather with return_exceptions
    print("\nExample 2: gather with return_exceptions")
    tasks = [
        risky_operation(1, False),  # Will succeed
        risky_operation(1, True),   # Will fail
        risky_operation(2, False),  # Will succeed
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Task {i} failed: {result}")
        else:
            print(f"Task {i} succeeded: {result}")
    
    # Example 3: Timeout handling
    print("\nExample 3: Timeout handling")
    try:
        # This will timeout after 0.5 seconds
        result = await asyncio.wait_for(risky_operation(2, False), timeout=0.5)
        print(f"Result: {result}")
    except asyncio.TimeoutError:
        print("Operation timed out!")
    
    # Example 4: Shielding from cancellation
    print("\nExample 4: Shielding critical operations")
    async def critical_operation():
        print("Starting critical operation...")
        await asyncio.sleep(2)
        print("Critical operation completed")
        return "Critical result"
    
    async def caller():
        # Create task for critical operation
        critical_task = asyncio.create_task(critical_operation())
        
        # Give it a moment to start
        await asyncio.sleep(0.5)
        
        # Try to cancel it
        print("Attempting to cancel critical task...")
        critical_task.cancel()
        
        try:
            result = await critical_task
            print(f"Result: {result}")
        except asyncio.CancelledError:
            print("Critical task was cancelled")
        except Exception as e:
            print(f"Critical task failed with: {e}")
    
    await caller()

# Rate Limiting Example
RATE_LIMITING = '''
import asyncio
import time

class RateLimiter:
    """Token bucket rate limiter for async operations."""
    
    def __init__(self, max_tokens: int, refill_rate: float):
        """
        Args:
            max_tokens: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """Acquire a token, waiting if necessary."""
        async with self._lock:
            now = time.time()
            # Add tokens based on time passed
            tokens_to_add = (now - self.last_refill) * self.refill_rate
            self.tokens = min(self.max_tokens, self.tokens + tokens_to_add)
            self.last_refill = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                # Need to wait for tokens to refill
                wait_time = (1 - self.tokens) / self.refill_rate
                await asyncio.sleep(wait_time)
                # Retry after waiting
                return await self.acquire()

# Usage example
async def rate_limited_fetch(session: aiohttp.ClientSession, url: str, limiter: RateLimiter):
    """Fetch URL with rate limiting."""
    await limiter.acquire()  # Wait for permission
    async with session.get(url) as response:
        return await response.text()

async def rate_limiting_example():
    """Example of rate limiting with AsyncIO."""
    limiter = RateLimiter(max_tokens=5, refill_rate=2.0)  # 5 tokens, refill 2 per second
    
    urls = [f'https://httpbin.org/delay/{i}' for i in range(1, 4)]
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            rate_limited_fetch(session, url, limiter)
            for url in urls
        ]
        
        results = await asyncio.gather(*tasks)
        print(f"Fetched {len(results)} URLs with rate limiting")
        return results
'''

def print_asyncio_examples():
    """Print AsyncIO examples for reference."""
    print("=== ASYNCIO BASICS ===")
    print(ASYNCIO_BASICS.strip())
    print("\n=== BASIC ASYNC/AWAIT EXAMPLES ===")
    print(BASIC_ASYNC_EXAMPLES.strip())
    print("\n=== ASYNC CONTEXT MANAGERS ===")
    print(ASYNC_CONTEXT_MANAGERS.strip())
    print("\n=== ASYNC ITERATORS ===")
    print(ASYNC_ITERATORS.strip())
    print("\n=== AIOHTTP EXAMPLES ===")
    print(AIOHTTP_EXAMPLES.strip())
    print("\n=== ERROR HANDLING ===")
    print(ERROR_HANDLING.strip())
    print("\n=== ERROR HANDLING EXAMPLES ===")
    print(ERROR_HANDLING_EXAMPLES.strip())
    print("\n=== RATE LIMITING ===")
    print(RATE_LIMITING.strip())

if __name__ == "__main__":
    print_asyncio_examples()
    
    # AsyncIO Interview Tips
    print("\n" + "="*50)
    print("ASYNCIO INTERVIEW TIPS:")
    print("="*50)
    print("1. Understand the event loop concept and how it works")
    print("2. Know the difference between async def and regular functions")
    print("3. Understand await keyword and what it can await")
    print("4. Be able to create and manage tasks with asyncio.create_task()")
    print("5. Know how to run coroutines concurrently with gather() and wait()")
    print("6. Understand async context managers (__aenter__, __aexit__)")
    print("7. Be familiar with async iterators (__aiter__, __anext__)")
    print("8. Know how to handle errors and exceptions in async code")
    print("9. Understand timeout handling with wait_for() and shield()")
    print("10. Be familiar with aiohttp for async HTTP requests")
    print("11. Understand when to use AsyncIO vs threading vs multiprocessing")
    print("12. Know about cancellation and how to handle CancelledError")
    print("13. Practice explaining the benefits of async I/O for network operations")
    print("14. Understand the concept of "event loop blocking" and how to avoid it")