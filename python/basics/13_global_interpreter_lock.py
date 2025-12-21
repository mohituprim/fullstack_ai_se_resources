"""
Global Interpreter Lock (GIL) in Python
======================================

What is the GIL?
----------------
The Global Interpreter Lock (GIL) is a mutex (a global lock) used by the
standard CPython interpreter that allows only ONE thread at a time to execute
Python bytecode.

Key points:
- Only one thread executes Python code at a time in a single process.
- Threads can still run concurrently, but the GIL ensures only one thread is
  "owning" the interpreter at any moment.
- This simplifies memory management (especially reference counting) and keeps
  the interpreter implementation simpler and safer.

When is the GIL a problem?
--------------------------
- For **CPU-bound** tasks (heavy computations in pure Python):
  - Multiple threads do NOT give true parallel speedup (on CPython).
  - The GIL forces them to take turns running on the CPU.
- For **I/O-bound** tasks (network requests, disk I/O, waiting):
  - Threads can still be very useful.
  - While one thread waits for I/O, another thread can run.

How to bypass or reduce GIL impact?
-----------------------------------
- Use `multiprocessing` (multiple processes, each with its own Python interpreter
  and GIL) for CPU-bound work.
- Use native extensions (C, Cython, NumPy, etc.) that can release the GIL during
  heavy computations.
- Use `asyncio` for high-concurrency I/O-bound tasks without creating many threads.

Below are small examples to illustrate GIL effects.
"""

import threading
import time


def cpu_bound_work(n: int) -> int:
    """
    A naive CPU-bound function: sum of squares.
    Used to simulate heavy computation in pure Python.
    """
    total = 0
    for i in range(n):
        total += i * i
    return total


def single_thread_cpu_demo() -> None:
    """
    Run CPU-bound work in a single thread.
    """
    start = time.time()
    cpu_bound_work(50_000_00)  # adjust this if it runs too fast/slow
    end = time.time()
    print(f"Single thread CPU demo took: {end - start:.3f} seconds")


def multi_thread_cpu_demo() -> None:
    """
    Run CPU-bound work in two threads and compare with the single-thread run.

    Because of the GIL, this will often NOT be significantly faster than the
    single-thread version for pure Python CPU-bound code.
    """
    start = time.time()

    t1 = threading.Thread(target=cpu_bound_work, args=(50_000_00,))
    t2 = threading.Thread(target=cpu_bound_work, args=(50_000_00,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end = time.time()
    print(f"Two threads CPU demo took: {end - start:.3f} seconds")


def io_bound_work(delay: float) -> None:
    """
    A simple I/O-bound function: just sleeps to simulate I/O wait.
    """
    time.sleep(delay)


def multi_thread_io_demo() -> None:
    """
    Demonstrate that threads help with I/O-bound tasks despite the GIL.

    Two threads both sleeping should take roughly the max of their delays,
    not the sum, because they can overlap while waiting.
    """
    start = time.time()

    t1 = threading.Thread(target=io_bound_work, args=(2,))
    t2 = threading.Thread(target=io_bound_work, args=(2,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end = time.time()
    print(f"Two threads I/O demo took: {end - start:.3f} seconds")


if __name__ == "__main__":
    print("=== Global Interpreter Lock (GIL) demos ===")
    single_thread_cpu_demo()
    multi_thread_cpu_demo()
    multi_thread_io_demo()


