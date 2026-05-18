from functools import wraps
import datetime

def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from tkinter import messagebox
            error_msg = f"Error in {func.__name__}: {str(e)}"
            print(f"[CRITICAL] {error_msg}")
            messagebox.showerror("Application Error", error_msg)
            return None
    return wrapper

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [ACTION] Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper