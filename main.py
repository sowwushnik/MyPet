import tkinter as tk
from gui_app import PetApp

def main():
    root = tk.Tk()
    app = PetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()