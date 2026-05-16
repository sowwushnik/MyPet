from functools import wraps

def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("System Error", f"An error occurred: {str(e)}")
            return None
    return wrapper

def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Action triggered: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper