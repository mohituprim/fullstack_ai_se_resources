# Robustness: Effective Python Best Practices

## 1. Take Advantage of Each Block in try/except/else/finally

### Explanation
Python’s `try` statement has **four parts**:
- `try`: code that might raise an exception
- `except`: handle specific errors
- `else`: runs **only if no exception** was raised in `try`
- `finally`: runs **always**, whether an exception occurred or not

Using all blocks correctly makes error-handling code clearer and safer.

### Use Cases
- Clean error handling with clear success vs. failure paths
- Ensuring resources are released (files, locks, DB connections)
- Separating “normal path” from “error path”

### Examples

```python
def read_config(path):
    try:
        f = open(path, "r", encoding="utf-8")
    except FileNotFoundError:
        # except: handle specific error
        return {"debug": False}  # default config
    else:
        # else: only if open() succeeded (no exception)
        import json
        return json.load(f)
    finally:
        # finally: always runs if f was created
        try:
            f.close()
        except UnboundLocalError:
            # f was never assigned (open failed before creating f)
            pass
```

More idiomatic (using `with`) but shows the role of each block:

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    else:
        # Only runs if no exception in try
        print("Division succeeded")
        return result
    finally:
        # Always runs
        print("Cleaning up, logging, etc.")
```

### Best Practices
- Put **only the code that can fail** in `try`, not the whole function
- Use `else` for code that should run **only when no exception** occurs
- Use `finally` for **unconditional cleanup** (closing files, releasing locks)

---

## 2. assert Internal Assumptions and raise Missed Expectations

### Explanation
`assert` is for **internal invariants** that should always be true if your code is correct. For user errors and invalid input, you should **raise explicit exceptions**, not rely on `assert`.

### Use Cases
- Documenting assumptions in algorithms
- Catching programmer mistakes early in development
- Checking impossible states (“this should never happen”)

### Examples

```python
def normalize(values):
    total = sum(values)
    # Internal assumption: total should not be zero here
    assert total != 0, "normalize: total must not be zero"
    return [v / total for v in values]

# ❌ BAD: Using assert for user input validation
def set_age(age):
    assert age >= 0, "age must be non-negative"  # can be removed with -O
    ...

# ✅ GOOD: Raise explicit exception for invalid input
def set_age(age):
    if age < 0:
        raise ValueError("age must be non-negative")
    ...
```

### Important Note
- Running Python with optimization (`python -O`) **removes asserts**. Never use them for user-facing validation or security checks.
- Use `assert`:
  - Inside private functions
  - For invariants and impossible states
- Use `raise` + specific exception:
  - For invalid user input
  - For contract violations at API boundaries

---

## 3. Consider contextlib and with Statements for Reusable try/finally Behavior

### Explanation
`try/finally` is often used to ensure resources are cleaned up. The `with` statement and `contextlib` help you **encapsulate** that pattern:
- `with` calls `__enter__` and `__exit__`
- `contextlib.contextmanager` lets you write **generator-based** context managers

### Use Cases
- Opening/closing files or network connections
- Acquiring/releasing locks
- Temporarily changing environment (cwd, environment variables, logging level)

### Examples

```python
# Without with/contextmanager
lock.acquire()
try:
    do_something()
finally:
    lock.release()

# With built-in context manager
from threading import Lock

lock = Lock()
with lock:
    do_something()
```

Custom context manager with `contextlib.contextmanager`:

```python
import contextlib
import time

@contextlib.contextmanager
def timed(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{label} took {end - start:.3f}s")

with timed("heavy work"):
    heavy_computation()
```

File-like resource:

```python
@contextlib.contextmanager
def open_db_connection(dsn):
    conn = connect_to_db(dsn)
    try:
        yield conn
    finally:
        conn.close()

with open_db_connection("postgres://...") as conn:
    conn.execute("SELECT 1")
```

### Benefits
- Fewer `try/finally` blocks scattered through code
- Clear, reusable resource management
- Less chance of forgetting cleanup

---

## 4. Always Make try Blocks as Short as Possible

### Explanation
If your `try` block is too big, it’s hard to tell **which line** raised the exception. That can:
- Hide real bugs
- Make debugging much harder

Keep the `try` around **exactly what may fail**, and nothing more.

### Examples

```python
import json

data = '{"name": "Alice"}'

# ❌ BAD: Huge try block
try:
    obj = json.loads(data)
    print("Parsed JSON")
    do_other_work(obj)        # if this raises, it's caught unintentionally
except json.JSONDecodeError:
    print("Invalid JSON")

# ✅ GOOD: Narrow try block
try:
    obj = json.loads(data)
except json.JSONDecodeError:
    print("Invalid JSON")
else:
    print("Parsed JSON")
    do_other_work(obj)        # errors here are real bugs, not JSON issues
```

Another example:

```python
# ❌ BAD
try:
    conn = open_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    process_users(users)
    conn.close()
except Exception as e:
    log_error(e)

# ✅ GOOD
try:
    conn = open_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
except DatabaseError as e:
    log_db_error(e)
    return
else:
    process_users(users)
finally:
    conn.close()
```

### Rule of Thumb
- Each `try` should protect **one logical operation**
- If you’re catching `Exception` for a whole function, you probably need to rethink the structure

---

## 5. Beware of Exception Variables Disappearing

### Explanation
In Python 3, the exception variable in `except Exception as e:` is **cleared** after the block to avoid reference cycles. If you need to keep the exception for later (e.g., storing it), you must copy it.

### Examples

```python
saved_exceptions = []

for item in items:
    try:
        process(item)
    except Exception as e:
        # If we store 'e' directly, it's fine *here*, but don't rely on it later
        saved_exceptions.append(e)

for exc in saved_exceptions:
    print(type(exc), exc)
```

The subtle issue is more about **tracebacks** and `__context__` being cleared when `e` goes out of scope. If you need complete information, use `traceback` or `logging.exception` immediately inside the `except` block.

Better pattern:

```python
import traceback

errors = []

for item in items:
    try:
        process(item)
    except Exception:
        # Capture full traceback string now
        tb = traceback.format_exc()
        errors.append(tb)

for tb in errors:
    print(tb)
```

### Guidance
- Handle or log exceptions **inside** the `except` block
- If you must store them, store a **copy** of what you need (message, traceback)

---

## 6. Beware of Catching the Exception Class

### Explanation
Catching the base `Exception` (or worse, `BaseException`) swallows **all errors**, including:
- Programming bugs (TypeError, AttributeError, etc.)
- Unexpected failures you should fix, not hide

You should **catch specific exceptions** that you **expect** and know how to handle.

### Examples

```python
import json

data = "not-json"

# ❌ BAD: Catching all exceptions
try:
    obj = json.loads(data)
except Exception as e:
    print("Something went wrong", e)  # hides programming errors too

# ✅ GOOD: Catch specific error you expect
try:
    obj = json.loads(data)
except json.JSONDecodeError as e:
    print("Invalid JSON:", e)
```

Dangerous pattern:

```python
# ❌ BAD
try:
    risky_operation()
except Exception:
    pass  # silently ignore ALL errors
```

### Best Practices
- Catch **specific exceptions** (e.g., `ValueError`, `KeyError`, `OSError`)
- If you must catch `Exception`, re-raise unknown ones:

```python
try:
    risky_operation()
except (KnownError1, KnownError2) as e:
    handle_known_error(e)
except Exception:
    # Log and re-raise unexpected
    log_unexpected_error()
    raise
```

---

## 7. Understand the Difference Between Exception and BaseException

### Explanation
The exception hierarchy:
- `BaseException`
  - `Exception`  ← most of your errors
  - `SystemExit`
  - `KeyboardInterrupt`
  - `GeneratorExit`

You should **almost never** catch `BaseException`, because that will also catch `KeyboardInterrupt` (Ctrl+C) and `SystemExit`, preventing your program from exiting cleanly.

### Examples

```python
# ❌ BAD: Catching BaseException
try:
    run_app()
except BaseException:
    # This will also catch KeyboardInterrupt and SystemExit
    log("Something terrible happened")

# ✅ GOOD: Catch Exception for “normal” errors
try:
    run_app()
except Exception as e:
    log(f\"Unhandled error: {e}\")
    raise
```

### Guidelines
- Use `except Exception` (not `BaseException`) for generic app-level error logging
- Allow `KeyboardInterrupt` to propagate so users can stop the program with Ctrl+C

---

## 8. Use traceback for Enhanced Exception Reporting

### Explanation
The `traceback` module lets you:
- Capture full stack traces
- Format them as strings
- Log them for later analysis

This is much more useful than just printing `str(e)`.

### Use Cases
- Logging errors in servers/CLI tools
- Storing errors for later debugging
- Displaying helpful debug info in development

### Examples

```python
import traceback

try:
    risky_operation()
except Exception:
    # Print to console
    traceback.print_exc()
\n    # Or capture as string
    tb_str = traceback.format_exc()
    log_to_file(tb_str)
```

Using `logging`:

```python
import logging
\nlogger = logging.getLogger(__name__)

try:
    risky_operation()
except Exception:
    logger.exception("Unexpected error while running risky_operation")
    # logger.exception() automatically includes the traceback
```

### Benefits
- Full context for debugging (file, line, call stack)
- Easier to understand intermittent/production-only problems

---

## 9. Consider Explicitly Chaining Exceptions to Clarify Tracebacks

### Explanation
When you catch one exception and raise another, Python automatically sets `__context__` and shows **“During handling of the above exception, another exception occurred”**.  
You can also explicitly chain exceptions with `raise ... from ...` to show **cause**.

### Use Cases
- Wrapping low-level errors in higher-level ones
- Preserving original error context while adding more information

### Examples

```python
def read_config(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        # ✅ Explicit chaining
        raise RuntimeError(f\"Config file not found: {path}\") from e
```

The traceback will clearly show:
- The `RuntimeError` at a higher level
- The **original** `FileNotFoundError` as the cause

Suppressing the context:

```python
try:
    something()
except SomeError as e:
    # Raise a new exception without showing original context
    raise NewError(\"clean message\") from None
```

### Guidance
- Use `raise NewError(...) from e` when you want to show **both** layers (high- and low-level)
- Use `from None` when the low-level detail would confuse the user

---

## 10. Always Pass Resources into Generators and Have Callers Clean Them Up Outside

### Explanation
Generators should **not** open/own external resources (like files or DB connections) in a way that makes cleanup unclear.  
Instead:
- The **caller** opens the resource
- Pass it **into** the generator
- The caller is responsible for cleaning up (via `with` or `try/finally`)

### ❌ Bad Pattern

```python
def read_lines(path):
    f = open(path)      # generator owns the file
    for line in f:
        yield line
    # If iteration stops early or an exception occurs, f may never be closed
```

### ✅ Good Pattern

```python
def read_lines(f):
    for line in f:
        yield line

with open("data.txt", "r", encoding="utf-8") as f:
    for line in read_lines(f):
        process(line)
# File is always closed by the with-block
```

More complex example:

```python
def filtered_lines(f, keyword):
    for line in f:
        if keyword in line:
            yield line

with open("application.log") as f:
    for line in filtered_lines(f, "ERROR"):
        print(line, end="")
```

### Benefits
- Clear ownership of resources
- No hidden `open()` inside generators
- Easier to test (pass in StringIO, etc.)

---

## 11. Never Set __debug__ to False

### Explanation
`__debug__` is a special built-in constant:
- `True` by default
- Set to `False` only when Python is started with `-O` (optimize)
- Controls whether `assert` statements are executed

You should **never** assign to `__debug__` yourself; it’s **read-only** and intended for the interpreter.

### Examples

```python
import sys

print(__debug__)           # True (normally)
print(sys.flags.optimize)  # 0 (no -O)

# Running: python -O script.py
# __debug__ becomes False, asserts are stripped
```

### Guidance
- Don’t rely on changing `__debug__` at runtime (you can’t)
- Use `assert` for internal checks, assuming they may be removed
- Use real exceptions (`raise`) for important checks

---

## 12. Avoid exec and eval Unless You’re Building a Developer Tool

### Explanation
`exec` and `eval` execute arbitrary Python code from strings. They are:
- **Dangerous** (security risk if input is not fully trusted)
- Hard to reason about and debug
- Often a sign you should redesign the API/data structure

### Use Cases
- Developer tools (REPLs, debuggers, code runners)
- Metaprogramming where there’s truly no better alternative

### Examples

```python
# ❌ BAD: Evaluating user input
user_code = input("Enter a Python expression: ")
result = eval(user_code)  # Security nightmare

# ✅ GOOD: Parse data instead of executing it
import json

data = json.loads(user_input_json)  # Safe (relatively), structured
```

Safer alternatives:
- Use **data formats** (`json`, `yaml`, `toml`) instead of Python code
- Use **dispatch tables** instead of dynamic code:

```python
def op_add(a, b): return a + b
def op_sub(a, b): return a - b

ops = {"+": op_add, "-": op_sub}

symbol = "+"
result = ops[symbol](1, 2)  # No eval needed
```

### Guidance
- Avoid `exec`/`eval` in application code
- If you must use them (e.g., a teaching tool / REPL), **never** pass untrusted input directly

---

## Summary

These twelve principles help you write **robust, safe, and debuggable** Python code:

1. **Use all parts of try/except/else/finally** – keep cleanup and success paths clear  
2. **Use assert for internal invariants**, raise explicit exceptions for user errors  
3. **Use contextlib and with** – encapsulate try/finally patterns for resource management  
4. **Keep try blocks small** – only wrap the code that can fail  
5. **Handle exceptions where they occur** – don’t rely on exception variables later  
6. **Don’t catch Exception blindly** – catch specific errors you can handle  
7. **Know Exception vs BaseException** – don’t swallow interrupts and exits  
8. **Use traceback/logging** for rich error reporting  
9. **Chain exceptions explicitly** to preserve error context  
10. **Let callers own resources** when using generators  
11. **Don’t touch `__debug__`**, and know asserts may be removed  
12. **Avoid exec/eval** unless you’re explicitly building tooling for code execution  

Always prioritize **clarity, safety, and good error reporting** over cleverness. Well-structured error handling makes your programs much easier to maintain and debug.
