import tkinter as tk
from tkinter import messagebox, ttk
from utils.decorators import handle_error, log_action
from models.pet import Dog, Cat
import json
import os


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("MyPet Pro")
        self.root.geometry("360x700")
        self.root.configure(bg="#F4F7F6")

        self.colors = {
            "orange": "#FF7800",
            "blue": "#133CAC",
            "teal": "#028E9B",
            "red": "#E74C3C",
            "white": "#FFFFFF",
            "text": "#2C3E50"
        }

        # --- HEADER ---
        header = tk.Frame(self.root, bg=self.colors["orange"], padx=20, pady=30)
        header.pack(fill=tk.X)

        tk.Label(header, text="Good morning, Meirkhan!", font=("Segoe UI", 18, "bold"),
                 fg="white", bg=self.colors["orange"]).pack(anchor="w")
        tk.Label(header, text="Everything is under control 🐾", font=("Segoe UI", 10),
                 fg="white", bg=self.colors["orange"]).pack(anchor="w")

        # --- BODY ---
        body = tk.Frame(self.root, bg="#F4F7F6", padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="QUICK NAVIGATION", font=("Segoe UI", 8, "bold"),
                 fg="#95A5A6", bg="#F4F7F6").pack(anchor="w", pady=(0, 10))

        # CARDS (English Labels)
        self.add_mobile_card(body, "🐕 MY PETS", "Database & Profiles", self.colors["blue"], self.open_database)
        self.add_mobile_card(body, "📊 HEALTH", "Weight & Activity", self.colors["teal"],
                             lambda: messagebox.showinfo("Info", "Health module coming soon!"))
        self.add_mobile_card(body, "📍 VET MAP", "Find nearby clinics", self.colors["red"],
                             lambda: messagebox.showinfo("Info", "Map loading..."))
        self.add_mobile_card(body, "🚪 EXIT", "Close Application", "#7F8C8D", self.root.quit)

    def add_mobile_card(self, master, title, sub, color, command):
        card = tk.Frame(master, bg="white", cursor="hand2", pady=15, padx=15)
        card.pack(fill=tk.X, pady=8)
        tk.Frame(card, bg=color, width=4).pack(side=tk.LEFT, fill=tk.Y)

        txt_frame = tk.Frame(card, bg="white", padx=10)
        txt_frame.pack(side=tk.LEFT)

        t_lbl = tk.Label(txt_frame, text=title, font=("Segoe UI", 11, "bold"), fg=color, bg="white")
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(txt_frame, text=sub, font=("Segoe UI", 9), fg="#95A5A6", bg="white")
        s_lbl.pack(anchor="w")

        a_lbl = tk.Label(card, text="→", font=("Segoe UI", 14), fg="#BDC3C7", bg="white")
        a_lbl.pack(side=tk.RIGHT)

        def on_click(e):
            card.configure(relief=tk.SUNKEN)
            self.root.after(100, lambda: card.configure(relief=tk.FLAT))
            command()

        for w in [card, txt_frame, t_lbl, s_lbl, a_lbl]:
            w.bind("<Button-1>", on_click)

    def open_database(self):
        PetApp(tk.Toplevel(self.root))


class PetApp:
    def __init__(self, window):
        self.window = window
        self.window.title("My Pets")
        self.window.geometry("360x700")
        self.window.configure(bg="#F4F7F6")
        self.window.grab_set()

        self.colors = {
            "primary": "#FF7800",
            "secondary_b": "#133CAC",
            "accent": "#028E9B",
            "white": "#FFFFFF",
            "text_gray": "#95A5A6"
        }

        # --- HEADER ---
        header = tk.Frame(self.window, bg=self.colors["secondary_b"], padx=20, pady=25)
        header.pack(fill=tk.X)

        tk.Label(header, text="MY PETS", font=("Segoe UI", 16, "bold"),
                 fg="white", bg=self.colors["secondary_b"]).pack(side=tk.LEFT)

        tk.Button(header, text="✕", font=("Segoe UI", 12, "bold"), fg="white",
                  bg=self.colors["secondary_b"], relief=tk.FLAT, cursor="hand2",
                  command=self.window.destroy).pack(side=tk.RIGHT)

        # --- ACTION BUTTONS ---
        top_btns = tk.Frame(self.window, bg="#F4F7F6", pady=15)
        top_btns.pack(fill=tk.X, padx=20)

        tk.Button(top_btns, text="+ DOG", bg=self.colors["primary"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT, width=15, pady=8,
                  command=lambda: self.add_pet_window("Dog")).pack(side=tk.LEFT, expand=True, padx=5)

        tk.Button(top_btns, text="+ CAT", bg=self.colors["secondary_b"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT, width=15, pady=8,
                  command=lambda: self.add_pet_window("Cat")).pack(side=tk.LEFT, expand=True, padx=5)

        # --- SCROLLABLE CONTENT ---
        self.canvas = tk.Canvas(self.window, bg="#F4F7F6", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F4F7F6")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=340)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.pets = self.load_pets()
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        if not self.pets:
            tk.Label(self.scrollable_frame, text="No pets registered yet",
                     bg="#F4F7F6", fg=self.colors["text_gray"], pady=50).pack()
            return
        for idx, pet in enumerate(self.pets):
            self.add_pet_card(pet, idx)

    def add_pet_card(self, pet, index):
        card = tk.Frame(self.scrollable_frame, bg="white", pady=15, padx=15)
        card.pack(fill=tk.X, pady=8)

        icon = "🐕" if isinstance(pet, Dog) else "🐈"

        info = tk.Frame(card, bg="white")
        info.pack(side=tk.LEFT)
        tk.Label(info, text=icon, font=("Segoe UI", 22), bg="white").pack(side=tk.LEFT, padx=(0, 10))

        txt = tk.Frame(info, bg="white")
        txt.pack(side=tk.LEFT)
        tk.Label(txt, text=pet.name.upper(), font=("Segoe UI", 10, "bold"), fg=self.colors["secondary_b"],
                 bg="white").pack(anchor="w")
        tk.Label(txt, text=f"{pet.breed} • {pet.age} yrs", font=("Segoe UI", 8), fg=self.colors["text_gray"],
                 bg="white").pack(anchor="w")

        btns = tk.Frame(card, bg="white")
        btns.pack(side=tk.RIGHT)
        tk.Button(btns, text="VIEW", font=("Segoe UI", 8, "bold"), fg=self.colors["accent"], bg="white", relief=tk.FLAT,
                  command=lambda p=pet: self.show_details(p)).pack()
        tk.Button(btns, text="DELETE", font=("Segoe UI", 7), fg="#E74C3C", bg="white", relief=tk.FLAT,
                  command=lambda i=index: self.remove_pet(i)).pack()

    @handle_error
    def add_pet_window(self, pet_type):
        win = tk.Toplevel(self.window)
        win.title(f"New {pet_type}")
        win.geometry("340x600")
        win.configure(bg="white")
        win.grab_set()

        color = self.colors["primary"] if pet_type == "Dog" else self.colors["secondary_b"]
        tk.Label(win, text=f"REGISTER {pet_type.upper()}", bg=color, fg="white", font=("Segoe UI", 12, "bold"),
                 pady=20).pack(fill=tk.X)

        fields = [("Name", "Buddy"), ("Age", "1"), ("Weight", "5.0"), ("Breed", "Poodle"), ("Temper", "Calm")]
        entries = {}
        for f, p in fields:
            tk.Label(win, text=f.upper(), bg="white", fg=self.colors["text_gray"], font=("Segoe UI", 8, "bold")).pack(
                anchor="w", padx=30, pady=(10, 0))
            e = tk.Entry(win, bg="#F4F7F6", relief=tk.FLAT)
            e.pack(fill=tk.X, padx=30, ipady=8)
            entries[f] = e

        def save():
            cls = Dog if pet_type == "Dog" else Cat
            new_pet = cls(entries["Name"].get(), int(entries["Age"].get()), float(entries["Weight"].get()),
                          entries["Breed"].get(), entries["Temper"].get())
            self.pets.append(new_pet)
            self.save_pets()
            self.refresh_list()
            win.destroy()

        tk.Button(win, text="SAVE PROFILE", bg=self.colors["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, command=save, pady=12).pack(fill=tk.X, padx=30, pady=30)

    def show_details(self, pet):
        profile = tk.Toplevel(self.window)
        profile.geometry("340x600")
        profile.configure(bg="#F4F7F6")

        color = self.colors["primary"] if isinstance(pet, Dog) else self.colors["secondary_b"]
        header = tk.Frame(profile, bg=color, pady=30)
        header.pack(fill=tk.X)
        tk.Label(header, text=pet.name.upper(), font=("Segoe UI", 18, "bold"), fg="white", bg=color).pack()
        tk.Label(header, text="HEALTH SUMMARY", font=("Segoe UI", 8), fg="white", bg=color).pack()

        card = tk.Frame(profile, bg="white", padx=20, pady=20)
        card.pack(fill=tk.X, padx=20, pady=20)

        details = [("Type", pet.__class__.__name__), ("Breed", pet.breed), ("Weight", f"{pet.weight} kg"),
                   ("Calories", f"{pet.calculate_daily_calories():.0f} kcal")]
        for l, v in details:
            row = tk.Frame(card, bg="white", pady=5)
            row.pack(fill=tk.X)
            tk.Label(row, text=l, fg=self.colors["text_gray"], bg="white").pack(side=tk.LEFT)
            tk.Label(row, text=v, fg=self.colors["secondary_b"], font=("Segoe UI", 9, "bold"), bg="white").pack(
                side=tk.RIGHT)
            tk.Frame(card, bg="#F4F7F6", height=1).pack(fill=tk.X, pady=5)

        tk.Button(profile, text="BACK TO LIST", bg=self.colors["secondary_b"], fg="white", relief=tk.FLAT,
                  command=profile.destroy, pady=10).pack(fill=tk.X, padx=20)

    def load_pets(self):
        if not os.path.exists("pets_data.json"): return []
        try:
            with open("pets_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                cls = Dog if item.get("type") == "Dog" else Cat
                loaded.append(cls(item["name"], item["age"], item["weight"], item["breed"], item["temperament"]))
            return loaded
        except:
            return []

    def save_pets(self):
        data = [p.to_dict() for p in self.pets]
        with open("pets_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def remove_pet(self, index):
        if messagebox.askyesno("Confirm", f"Delete {self.pets[index].name}?"):
            self.pets.pop(index)
            self.save_pets()
            self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()