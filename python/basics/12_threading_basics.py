"""
Threading basics in Python.

This file demonstrates:
- Creating and starting threads
- Waiting for threads to finish (join)
- Sharing data safely between threads using a Lock

Threading is best for I/O-bound tasks (network calls, disk I/O, waiting, etc.),
not CPU-heavy computations (because of the Global Interpreter Lock, GIL).
"""

import threading
import time


def worker(name: str, delay: float) -> None:
    """
    Simple worker function to demonstrate basic threading.
    It prints a start message, sleeps, then prints a finish message.
    """
    print(f"[{name}] starting")
    time.sleep(delay)  # simulate some work (I/O, waiting, etc.)
    print(f"[{name}] finished after {delay} seconds")


def basic_thread_example() -> None:
    """
    Create and start multiple threads, then wait for them to complete.
    """
    t1 = threading.Thread(target=worker, args=("Thread-1", 2))
    t2 = threading.Thread(target=worker, args=("Thread-2", 1))

    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()

    print("All threads completed (basic example)")


# ---------------------------------------------------------------------------
# Shared data and race conditions
# ---------------------------------------------------------------------------

counter = 0
counter_lock = threading.Lock()


def increment(n: int) -> None:
    """
    Increment a shared counter n times in a thread-safe way.
    Using a Lock prevents race conditions.
    """
    global counter
    for _ in range(n):
        # Critical section: only one thread can execute this block at a time.
        with counter_lock:
            counter += 1


def shared_data_example() -> None:
    """
    Demonstrate safe updates to a shared variable using a Lock.
    """
    global counter
    counter = 0

    t1 = threading.Thread(target=increment, args=(100_000,))
    t2 = threading.Thread(target=increment, args=(100_000,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    # With the lock, this will reliably print 200000
    print("Counter =", counter)


if __name__ == "__main__":
    print("=== Basic threading demo ===")
    basic_thread_example()

    print("\n=== Shared data with Lock demo ===")
    shared_data_example()


