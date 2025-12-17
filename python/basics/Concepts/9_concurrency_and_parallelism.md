# Concurrency and Parallelism: Effective Python Best Practices

## 1. Use subprocess to Manage Child Processes

### Explanation
The `subprocess` module lets you start external programs (child processes) from Python, capture their output, and manage their lifecycle. This is useful when:
- You need to call existing command-line tools
- You want to run separate OS-level processes (true parallelism across CPU cores)
- You need isolation from your main Python process

### Use Cases
- Running system commands (e.g., `ffmpeg`, `git`, `ls`)
- Offloading heavy work to another program
- Integrating with tools written in other languages
- Supervising worker processes (start, monitor, restart)

### Examples

```python
import subprocess

# Simple command, wait for completion
result = subprocess.run(
    ["echo", "Hello from subprocess"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout.strip())  # "Hello from subprocess"

# Run external tool and check exit code
try:
    subprocess.run(["ls", "-l", "/nonexistent"], check=True)
except subprocess.CalledProcessError as exc:
    print(f"Command failed with exit code {exc.returncode}")

# Capture stdout and stderr
proc = subprocess.run(
    ["python3", "-c", "print('hi'); raise SystemExit(1)"],
    capture_output=True,
    text=True,
)
print("stdout:", proc.stdout)
print("stderr:", proc.stderr)
print("code:", proc.returncode)

# Long-running process (e.g., server)
server_proc = subprocess.Popen(
    ["python3", "-m", "http.server", "8000"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

# ... do other work ...

# Terminate the server when done
server_proc.terminate()
server_proc.wait()
```

### When to Use subprocess
- ✅ You need **true parallelism** across CPU cores by spawning separate processes
- ✅ You want to call an existing CLI tool rather than rewriting it in Python
- ✅ You need isolation from the main Python process (crashes, memory usage)
- ❌ You only need to run Python code concurrently inside the same process (use threads/asyncio instead)

---

## 2. Use Threads for Blocking I/O; Avoid for Parallelism

### Explanation
Python threads are best for **blocking I/O-bound tasks** (network, disk, APIs), not for CPU-bound parallelism, because of the **GIL (Global Interpreter Lock)**. The GIL means only one thread executes Python bytecode at a time per process.

### Use Cases
- Concurrent HTTP requests
- Reading/writing many files concurrently
- Waiting on slow network or database calls

### Examples

```python
import threading
import time
import requests

urls = [
    "https://example.com",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
]

def fetch(url):
    print(f"Starting {url}")
    resp = requests.get(url)
    print(f"Done {url}: {resp.status_code}")

# ❌ BAD: Sequential (slow for I/O)
def fetch_all_sequential():
    for url in urls:
        fetch(url)

# ✅ GOOD: Threads for I/O
def fetch_all_threaded():
    threads = []
    for url in urls:
        t = threading.Thread(target=fetch, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

start = time.time()
fetch_all_threaded()
print("Total time:", time.time() - start)
```

### Why Avoid Threads for CPU-bound Parallelism

```python
import threading

def cpu_heavy(n):
    total = 0
    for i in range(10_000_000):
        total += (i * n) % 7
    return total

def run_threads():
    threads = []
    for _ in range(4):
        t = threading.Thread(target=cpu_heavy, args=(5,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

# This will NOT scale well across cores because of the GIL.
```

For CPU-bound work, use **`multiprocessing` or `concurrent.futures.ProcessPoolExecutor`** instead of threads.

---

## 3. Use Lock to Prevent Data Races in Threads

### Explanation
When multiple threads modify shared data concurrently, you can get **data races** and corrupted state. Use `threading.Lock` (or `RLock`) to protect critical sections so that only one thread manipulates the shared data at a time.

### Use Cases
- Incrementing shared counters
- Updating shared dictionaries/lists
- Writing to shared resources (e.g., single log file)

### Examples

```python
import threading

counter = 0
lock = threading.Lock()

def increment_many(times):
    global counter
    for _ in range(times):
        # ❌ BAD: No lock – race condition
        # counter += 1

        # ✅ GOOD: Protect with lock
        with lock:
            counter += 1

threads = [threading.Thread(target=increment_many, args=(100_000,)) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("Final counter:", counter)  # With lock: 1_000_000; without lock: unpredictable
```

### Best Practices
- Keep **critical sections short** (hold the lock for as little time as possible)
- Prefer `with lock:` context manager over `lock.acquire()` / `lock.release()`
- Avoid holding multiple locks at once (deadlock risk)

---

## 4. Use Queue to Coordinate Work Between Threads

### Explanation
`queue.Queue` is a **thread-safe** FIFO queue. It lets you pass work items from producer threads to worker threads safely, without manual locking.

### Use Cases
- Worker pools / consumer threads
- Background processing of tasks
- Logging pipelines

### Examples

```python
import threading
import queue
import time

task_queue = queue.Queue()

def worker(name):
    while True:
        task = task_queue.get()
        if task is None:   # Sentinel to shut down
            print(f"{name}: exiting")
            task_queue.task_done()
            break
        print(f"{name}: processing {task}")
        time.sleep(0.5)
        task_queue.task_done()

# Start workers
workers = []
for i in range(3):
    t = threading.Thread(target=worker, args=(f"worker-{i}",), daemon=True)
    t.start()
    workers.append(t)

# Enqueue tasks
for n in range(10):
    task_queue.put(n)

# Send sentinel to stop workers
for _ in workers:
    task_queue.put(None)

task_queue.join()  # Wait until all tasks are processed
```

### Benefits
- Built-in thread safety
- Backpressure via `maxsize` and `put()` blocking
- Clean shutdown using sentinel values (`None`, special objects)

---

## 5. Know How to Recognize When Concurrency Is Necessary

### Explanation
Concurrency adds complexity (locks, races, deadlocks, debugging difficulty). Use it **only when necessary**. Detect when your program is:
- **I/O-bound** (waiting on network/disk): concurrency can help a lot
- **CPU-bound**: consider process-based parallelism or algorithmic improvements
- **Latency-sensitive**: UI responsiveness, web servers, etc.

### Use Cases
- Many slow HTTP calls in parallel
- Background work in GUIs/web servers
- Processing streams of events (logs, messages)

### Examples

```python
import time
import requests

def download_all(urls):
    start = time.time()
    for url in urls:
        requests.get(url)  # Blocking I/O
    print("Sequential:", time.time() - start)

# If the program spends most of its time **waiting** (I/O-bound),
# concurrency (threads or asyncio) can drastically reduce total time.

def is_io_bound():
    # Rough heuristic: profile or log time spent in I/O vs CPU
    pass
```

### Heuristics
- Profile your code (e.g., `cProfile`) before adding concurrency
- If **CPU is mostly idle** while waiting → concurrency likely helpful
- If **CPU is near 100%** → optimize algorithm or use multiple processes

---

## 6. Avoid Creating New Thread Instances for On-demand Fan-out

### Explanation
Spawning a new `threading.Thread` for every task (e.g., every request) is expensive and can exhaust system resources. Instead, reuse a **fixed pool of worker threads**.

### Problem Example

```python
import threading

def handle_request(sock):
    # Handle a single client connection
    pass

def naive_server(listen_sock):
    while True:
        client_sock, _ = listen_sock.accept()
        # ❌ BAD: One new thread per client, unbounded
        t = threading.Thread(target=handle_request, args=(client_sock,))
        t.daemon = True
        t.start()
```

This can create thousands of threads under high load → memory pressure, context-switch overhead, instability.

### Better Approach: Worker Pool

```python
import queue
import threading

task_queue = queue.Queue()

def worker():
    while True:
        sock = task_queue.get()
        if sock is None:
            break
        handle_request(sock)
        task_queue.task_done()

def better_server(listen_sock, num_workers=20):
    # Start fixed workers
    workers = [threading.Thread(target=worker, daemon=True) for _ in range(num_workers)]
    for w in workers:
        w.start()
\n    while True:
        client_sock, _ = listen_sock.accept()
        task_queue.put(client_sock)
```

---

## 7. Understand How Using Queue for Concurrency Requires Refactoring

### Explanation
Introducing `queue.Queue` changes your program structure:
- Functions may no longer be called directly; they are **tasks** consumed by workers
- You often need a **producer/consumer** architecture
- Error handling and shutdown become more explicit (sentinels, joins)

### Before vs After

```python
# BEFORE: direct calls
def process_item(item):
    ...  # do work

items = [...]
for item in items:
    process_item(item)

# AFTER: queue-based workers
import queue, threading

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        try:
            process_item(item)
        finally:
            q.task_done()

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()

for item in items:
    q.put(item)

for _ in threads:
    q.put(None)

q.join()
```

### Key Changes
- Tasks are now **data** (in queues), not direct function calls
- Worker lifetime and graceful shutdown must be managed
- Exceptions in workers need to be logged/propagated explicitly

---

## 8. Consider ThreadPoolExecutor When Threads Are Necessary for Concurrency

### Explanation
`concurrent.futures.ThreadPoolExecutor` provides a higher-level API over raw threads and queues:
- Manages a pool of threads for you
- Lets you submit callables and get `Future` objects
- Handles lifecycle and shutdown cleanly

### Use Cases
- Parallelizing many I/O-bound tasks
- Simplifying thread-based code

### Examples

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

urls = [
    "https://example.com",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
]

def fetch(url):
    resp = requests.get(url)
    return url, resp.status_code

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch, url) for url in urls]
    for future in as_completed(futures):
        url, status = future.result()
        print(url, status)
```

### Benefits
- No manual thread creation
- Futures capture results and exceptions
- Easy to limit concurrency with `max_workers`

---

## 9. Achieve Highly Concurrent I/O with Coroutines

### Explanation
`asyncio` coroutines (`async def` / `await`) let you write **single-threaded, highly concurrent** I/O code. While one task waits for I/O, the event loop runs other tasks.

### Use Cases
- High-concurrency network servers/clients
- Many concurrent HTTP requests
- Chat servers, websockets, streaming

### Examples

```python
import asyncio
import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
]

async def fetch(session, url):
    async with session.get(url) as resp:
        print(url, resp.status)
        return await resp.text()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        await asyncio.gather(*tasks)

asyncio.run(main())
```

### Advantages over Threads for I/O
- Lower overhead (no thread per connection)
- Easier to scale to thousands of concurrent connections
- Deterministic concurrency model (single-threaded by default)

---

## 10. Know How to Port Threaded I/O to asyncio

### Explanation
To migrate from a threaded I/O model to `asyncio`:
1. Identify blocking calls (network, disk, sleep)
2. Replace them with their async equivalents (`aiohttp`, `asyncio.sleep`, async DB drivers)
3. Turn functions into `async def` and use `await`
4. Replace thread pools with `asyncio.gather` / tasks

### Example: Threaded → Async

```python
# BEFORE: threaded
import threading, requests

def fetch(url):
    resp = requests.get(url)
    return resp.text

def fetch_all(urls):
    results = []
    threads = []
    for url in urls:
        t = threading.Thread(target=lambda u=url: results.append(fetch(u)))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return results

# AFTER: asyncio + aiohttp
import asyncio, aiohttp

async def fetch_async(session, url):
    async with session.get(url) as resp:
        return await resp.text()

async def fetch_all_async(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_async(session, url) for url in urls]
        return await asyncio.gather(*tasks)

results = asyncio.run(fetch_all_async(urls))
```

---

## 11. Mix Threads and Coroutines to Ease the Transition to asyncio

### Explanation
Real-world apps often need a **hybrid** approach:
- Existing blocking libraries (e.g., a DB driver) that are not async
- New asyncio-based code

You can:
- Run blocking code in a **thread pool** from within async code (`asyncio.to_thread` or `loop.run_in_executor`)
- Use threads for CPU-bound or legacy parts while the rest is async

### Examples

```python
import asyncio
import time

def blocking_io():
    time.sleep(2)
    return "done blocking"

async def main():
    # ✅ Run blocking function in a thread without blocking the event loop
    result = await asyncio.to_thread(blocking_io)
    print(result)

asyncio.run(main())
```

You can also start an event loop in one thread and continue to use threads for other tasks, but keep the **event loop single-threaded**.

---

## 12. Maximize Responsiveness of asyncio Event Loops with async-friendly Worker Threads

### Explanation
Even in asyncio apps, some operations are:
- CPU-bound
- Blocking (no async version)

To keep the **event loop responsive**, offload such work to:
- `asyncio.to_thread()` (Python 3.9+)
- `loop.run_in_executor()` with a `ThreadPoolExecutor`

### Examples

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def cpu_heavy(n):
    total = 0
    for i in range(10_000_000):
        total += (i * n) % 7
    return total

async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=4) as pool:
        # Offload CPU-heavy work so event loop can keep handling I/O
        future = loop.run_in_executor(pool, cpu_heavy, 5)
        print("Doing other async work while CPU task runs...")
        result = await future
        print("CPU result:", result)

asyncio.run(main())
```

### Goal
- Keep the event loop **free** to schedule coroutines and handle I/O
- Offload blocking/CPU-heavy work to worker threads (or processes)

---

## 13. Consider concurrent.futures for True Parallelism

### Explanation
For **CPU-bound** tasks that need real parallel speedup across cores, use **process-based** execution:
- `concurrent.futures.ProcessPoolExecutor`
- `multiprocessing`

Each process has its own Python interpreter and GIL, so CPU-bound work can run in parallel.

### Use Cases
- Image processing
- Data crunching / numerical simulations
- Heavy CPU-bound computations

### Examples

```python
from concurrent.futures import ProcessPoolExecutor, as_completed

def cpu_heavy(n):
    total = 0
    for i in range(10_000_000):
        total += (i * n) % 7
    return total

numbers = [5, 10, 20, 30]

with ProcessPoolExecutor() as executor:
    futures = [executor.submit(cpu_heavy, n) for n in numbers]
    for fut in as_completed(futures):
        print("Result:", fut.result())
```

### Choosing the Right Tool
- **subprocess / ProcessPoolExecutor** → true parallelism, isolation, CPU-bound work
- **ThreadPoolExecutor / threads** → I/O-bound concurrency
- **asyncio coroutines** → high-concurrency I/O in a single thread

---

## Summary

These thirteen principles help you design correct and efficient concurrent Python programs:

1. **subprocess** – Use child processes to manage external commands and isolate work  
2. **Threads for I/O** – Use threads for blocking I/O, not CPU-bound parallelism  
3. **Locks** – Protect shared data from races in threaded code  
4. **Queues** – Coordinate producer/consumer work safely between threads  
5. **Recognize when concurrency is needed** – Profile and understand I/O vs CPU-bound behavior  
6. **Avoid per-task threads** – Use pools instead of unbounded thread creation  
7. **Refactor for queues** – Understand that queue-based concurrency changes your architecture  
8. **ThreadPoolExecutor** – Prefer it over manual threads for I/O concurrency  
9. **Coroutines** – Use asyncio for highly concurrent I/O in one thread  
10. **Porting to asyncio** – Replace blocking calls with async equivalents and `await`  
11. **Mix threads and coroutines** – Use thread pools from async code for legacy/blocking calls  
12. **Async-friendly worker threads** – Offload CPU/blocking tasks from the event loop  
13. **Process-based parallelism** – Use `concurrent.futures` processes for true CPU parallelism  

Always remember: **start with a simple, correct design; add concurrency only where it clearly improves performance or responsiveness.**
