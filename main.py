import tkinter as tk
from utils.storage import PetStorage
from gui_app import MainMenu

def main():
    storage = PetStorage()

    root = tk.Tk()

    app = MainMenu(root, storage)

    root.mainloop()

if __name__ == "__main__":
    main()