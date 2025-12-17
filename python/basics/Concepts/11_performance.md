# Performance: Effective Python Best Practices

## 1. Profile Before Optimizing

### Explanation
You should **never guess** where the performance bottleneck is. Always use a **profiler** to measure where time is really spent before you optimize. Most of the time, one or two hot spots dominate runtime.

### Use Cases
- Slow scripts or APIs
- Performance regressions after refactors
- Understanding where to invest optimization effort

### Examples

```python
# Simple usage with cProfile from the command line:
# python -m cProfile -o profile.out your_script.py

import cProfile
import pstats

def main():
    # Your program's main logic
    do_work()

if __name__ == "__main__":
    with cProfile.Profile() as pr:
        main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME).print_stats(20)  # top-20 functions by time
```

You can also profile a **single function**:

```python
def slow_function():
    ...

import cProfile

cProfile.run("slow_function()", sort="tottime")
```

### Best Practices
- Optimize **only after** you know the actual hot spots
- Focus on the **top few functions** that consume most of the time
- Re-run the profiler after changes to confirm improvement

---

## 2. Optimize Performance-Critical Code Using timeit Microbenchmarks

### Explanation
Once you know which small piece of code is hot, use `timeit` to compare alternative implementations in isolation. `timeit` runs code many times and reports reliable timings.

### Use Cases
- Comparing two loop implementations
- Testing effects of different data structures or algorithms
- Evaluating library calls vs custom code

### Examples

```python
import timeit

setup = "data = list(range(1000))"

stmt1 = "[x * 2 for x in data]"
stmt2 = "list(map(lambda x: x * 2, data))"

t1 = timeit.timeit(stmt1, setup=setup, number=50_000)
t2 = timeit.timeit(stmt2, setup=setup, number=50_000)

print("list comprehension:", t1)
print("map + lambda      :", t2)
```

From the command line:

```bash
python -m timeit "sum(range(1000))"
python -m timeit "total = 0\nfor i in range(1000): total += i"
```

### Guidelines
- Keep microbenchmarks **small and focused**
- Use realistic data sizes/types
- Beware of optimizing for microbenchmarks that don’t reflect real usage

---

## 3. Know When and How to Replace Python with Another Programming Language

### Explanation
Sometimes pure Python is **too slow** for the hottest inner loops, especially CPU-bound numeric or algorithmic code. In those cases:
- First, choose better algorithms / data structures
- If still too slow, offload the hot parts to:
  - C / C++ (via extensions, `ctypes`, `cffi`, Cython)
  - Rust, Go, or other languages via FFI or subprocesses

### Use Cases
- Heavy numeric computation
- Image/audio/video processing
- Tight loops that run millions of times

### Patterns
- **Option 1: Use libraries** that already wrap fast native code:
  - `numpy`, `pandas`, `scipy`, `pyarrow`, etc.
- **Option 2: subprocess** to call an external optimized tool
- **Option 3: C/C++/Rust extension** for critical inner loops

Example (calling a compiled binary via subprocess):

```python
import subprocess

def heavy_compute(input_path, output_path):
    # Assume 'my_fast_tool' is a compiled binary
    subprocess.run(
        ["my_fast_tool", input_path, output_path],
        check=True,
    )
```

### Decision Flow
1. Profile first – is it really **CPU-bound** and in pure Python?
2. Try **algorithmic** improvements and faster libraries (`numpy` etc.)
3. Only then consider rewriting the hot part in another language

---

## 4. Consider ctypes to Rapidly Integrate with Native Libraries

### Explanation
`ctypes` lets you call functions from C shared libraries directly from Python, without writing a full extension module. It’s a quick way to:
- Call existing C APIs
- Wrap optimized C code

### Use Cases
- Using system libraries (e.g., `libc`, OS APIs)
- Wrapping small C helpers for performance-critical parts

### Examples

```c
/* example.c */
int add(int a, int b) {
    return a + b;
}
```

Compile to a shared library (platform-specific, e.g. Linux):

```bash
gcc -shared -fPIC -o libexample.so example.c
```

Call it from Python:

```python
import ctypes

lib = ctypes.CDLL("./libexample.so")

lib.add.argtypes = (ctypes.c_int, ctypes.c_int)
lib.add.restype = ctypes.c_int

result = lib.add(2, 3)
print(result)  # 5
```

### Caveats
- You must get types (`argtypes`, `restype`) **exactly right**
- Crashes (segfaults) are possible if you misuse the API
- For larger projects, consider Cython, `cffi`, or full extension modules instead

---

## 5. Consider Extension Modules to Maximize Performance and Ergonomics

### Explanation
Extension modules (in C, C++, Cython, or Rust) let you:
- Write the hot loop in a compiled language
- Expose a clean Python API
- Achieve **C-level speed** while keeping most of the code in Python

### Use Cases
- Libraries that need both performance and a nice Python interface
- Heavily-used numeric or algorithmic code

### Sketch Example with Cython

```cython
# fast_sum.pyx
def fast_sum(int[:] arr):
    cdef Py_ssize_t i, n = arr.shape[0]
    cdef long total = 0
    for i in range(n):
        total += arr[i]
    return total
```

Then build it with a `setup.py` or `pyproject.toml`, and call from Python:

```python
import numpy as np
from fast_sum import fast_sum

arr = np.arange(10_000_000, dtype=np.int32)
print(fast_sum(arr))  # much faster than pure-Python loop
```

### Considerations
- More setup/maintenance overhead
- Great for library authors and performance-critical projects

---

## 6. Rely on Precompiled Bytecode and File System Caching to Improve Startup Time

### Explanation
When you import a module, Python compiles it to bytecode (`.pyc`) and stores it in `__pycache__`. On subsequent imports:
- If the `.py` file hasn’t changed, Python can **reuse** the `.pyc` file
- This speeds up startup and module import time

### Use Cases
- Large applications with many modules
- CLI tools or servers that import lots of code at startup

### Tips
- Don’t delete `__pycache__` folders unnecessarily in production
- Avoid doing heavy work at import time (top-level code); move it into `main()` or functions

Example of **bad import-time work**:

```python
# ❌ BAD: heavy work at import time
big_data = load_gigantic_dataset()  # runs whenever module is imported

def main():
    ...
```

Better:

```python
big_data = None

def main():
    global big_data
    if big_data is None:
        big_data = load_gigantic_dataset()
    ...
```

---

## 7. Lazy-Load Modules with Dynamic Imports to Reduce Startup Time

### Explanation
If some imports are only needed for rare code paths, you can **import them lazily** inside functions, not at the top of the file. This:
- Reduces initial startup time
- Defers cost until (and unless) functionality is actually used

### Use Cases
- Optional features (e.g., PDF export, plotting)
- Expensive libraries (e.g., `pandas`, `matplotlib`, `tensorflow`)

### Examples

```python
# Top-level imports (always loaded)
import json

def export_to_pdf(data, path):
    # Lazy import: only when this function is called
    import reportlab  # hypothetical heavy library
    ...

def maybe_plot(data, show_plot: bool):
    if show_plot:
        import matplotlib.pyplot as plt
        plt.plot(data)
        plt.show()
```

### Guidance
- Use lazy imports for **rarely used** or **heavy** modules
- Don’t overuse; too many dynamic imports can make code harder to read

---

## 8. Consider memoryview and bytearray for Zero-Copy Interactions with bytes

### Explanation
Copying large `bytes` objects is expensive. `memoryview` lets you create **views** into an existing bytes-like object **without copying**. `bytearray` is a mutable bytes type that works well with `memoryview`.

### Use Cases
- Parsing binary protocols
- Working with slices of large byte buffers
- Interfacing with I/O APIs that expect writable buffers

### Examples

```python
data = b"HEADER1234567890BODY"

# ❌ BAD: copying slices repeatedly
header = data[:6]   # new bytes object
body   = data[6:]   # another new bytes object

# ✅ GOOD: use memoryview to avoid copies
mv = memoryview(data)
header_view = mv[:6]
body_view   = mv[6:]

print(bytes(header_view))  # convert to bytes if needed
print(bytes(body_view))
```

Working with `bytearray`:

```python
buf = bytearray(b"abcdefghij")
mv = memoryview(buf)

mv[0:4] = b"ABCD"   # modifies underlying bytearray in-place
print(buf)          # bytearray(b'ABCDefghij')
```

Reading into a buffer (zero-copy style):

```python
import os

buf = bytearray(1024)
num_read = os.read(0, buf)  # read from stdin into existing buffer
view = memoryview(buf)[:num_read]
process_bytes(view)         # no extra copy
```

### Benefits
- Avoid unnecessary allocations and copies
- Improve performance for large or frequent binary operations

---

## Summary

These eight principles help you write **fast and efficient** Python code without premature or misguided optimization:

1. **Profile before optimizing** – always measure where time is actually spent  
2. **Use timeit for microbenchmarks** – compare alternative snippets in isolation  
3. **Know when to leave Python** – only after algorithmic fixes and profiling  
4. **Use ctypes (or similar) for native libraries** – integrate existing fast code  
5. **Consider extension modules** – C/Cython/Rust for critical hot paths  
6. **Leverage bytecode caching** – avoid heavy work at import time  
7. **Lazy-load heavy modules** – reduce startup cost for rarely used features  
8. **Use memoryview/bytearray** – zero-copy operations on byte data  

Always start with **clear, correct code**, measure with proper tools, and then optimize only where it really matters.
