import tkinter as tk
from tkinter import messagebox, ttk
from utils.decorators import handle_error
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

        # HEADER
        header = tk.Frame(self.root, bg=self.colors["orange"], padx=20, pady=30)
        header.pack(fill = tk.X)

        tk.Label(header, text="Good morning, Meirkhan!", font=("Segoe UI", 18, "bold"),
                 fg="white", bg=self.colors["orange"]).pack(anchor="w")
        tk.Label(header, text="Everything is under control 🐾", font=("Segoe UI", 10),
                 fg="white", bg=self.colors["orange"]).pack(anchor="w")

        # AVATARS
        avatar_frame = tk.Frame(header, bg=self.colors["orange"], pady=15)
        avatar_frame.pack(fill=tk.X)
        for icon in ["🐕", "🐈", "🐇"]:
            tk.Label(avatar_frame, text=icon, font=("Segoe UI", 18), bg="#FF9640", fg="white", width=2).pack(
                side=tk.LEFT, padx=5)

        body = tk.Frame(self.root, bg="#F4F7F6", padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="QUICK NAVIGATION", font=("Segoe UI", 8, "bold"),
                 fg="#95A5A6", bg="#F4F7F6").pack(anchor="w", pady=(0, 10))

        # CARDS
        self.add_mobile_card(body, "🐕 MY PETS", "Database & Profiles", self.colors["blue"], self.open_database)
        self.add_mobile_card(body, "📊 HEALTH", "Weight & Activity", self.colors["teal"],
                             lambda: messagebox.showinfo("Info", "Health charts..."))
        self.add_mobile_card(body, "📍 VET MAP", "Find nearby clinics", self.colors["red"],
                             lambda: messagebox.showinfo("Info", "Map loading..."))
        self.add_mobile_card(body, "🚪 EXIT", "Close App", "#7F8C8D", self.root.quit)

        # BOTTOM NAV
        nav_bar = tk.Frame(self.root, bg="white", height=60, highlightbackground="#ECF0F1", highlightthickness=1)
        nav_bar.pack(fill=tk.X, side=tk.BOTTOM)
        for icon, name in [("🏠", "Home"), ("🏥", "Health"), ("🔔", "Reminders"), ("🐾", "Profile")]:
            btn = tk.Frame(nav_bar, bg="white")
            btn.pack(side=tk.LEFT, expand=True)
            tk.Label(btn, text=icon, font=("Segoe UI", 14), bg="white").pack()
            tk.Label(btn, text=name, font=("Segoe UI", 7), bg="white", fg="#95A5A6").pack()

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
            "bg_light": "#F4F7F6",
            "white": "#FFFFFF",
            "text_gray": "#95A5A6"
        }

        # HEADER
        header = tk.Frame(self.window, bg=self.colors["secondary_b"], padx=20, pady=25)
        header.pack(fill=tk.X)

        tk.Label(header, text="MY PETS", font=("Segoe UI", 16, "bold"),
                 fg="white", bg=self.colors["secondary_b"]).pack(side=tk.LEFT)

        tk.Button(header, text="✕", font=("Segoe UI", 12, "bold"), fg="white",
                  bg=self.colors["secondary_b"], relief=tk.FLAT, cursor="hand2",
                  command=self.window.destroy).pack(side=tk.RIGHT)

        # BUTTONS
        top_btns = tk.Frame(self.window, bg="#F4F7F6", pady=15)
        top_btns.pack(fill=tk.X, padx=20)

        tk.Button(top_btns, text="+ ADD DOG", bg=self.colors["primary"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT, width=15, pady=8,
                  command=lambda: self.add_pet_window("Dog")).pack(side=tk.LEFT, expand=True, padx=5)

        tk.Button(top_btns, text="+ ADD CAT", bg=self.colors["secondary_b"], fg="white",
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT, width=15, pady=8,
                  command=lambda: self.add_pet_window("Cat")).pack(side=tk.LEFT, expand=True, padx=5)

        # SCROLLABLE LIST
        self.canvas = tk.Canvas(self.window, bg="#F4F7F6", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F4F7F6")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

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
                     bg="#F4F7F6", fg=self.colors["text_gray"], font=("Segoe UI", 10)).pack(pady=50)
            return

        for idx, pet in enumerate(self.pets):
            self.add_pet_card(pet, idx)

    def add_pet_card(self, pet, index):
        card = tk.Frame(self.scrollable_frame, bg="white", pady=15, padx=15)
        card.pack(fill=tk.X, pady=8)

        icon = "🐕" if isinstance(pet, Dog) else "🐈"
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side=tk.LEFT)

        tk.Label(info_frame, text=icon, font=("Segoe UI", 24), bg="white").pack(side=tk.LEFT, padx=(0, 10))

        txt_subframe = tk.Frame(info_frame, bg="white")
        txt_subframe.pack(side=tk.LEFT)

        tk.Label(txt_subframe, text=pet.name.upper(), font=("Segoe UI", 11, "bold"),
                 fg=self.colors["secondary_b"], bg="white").pack(anchor="w")
        tk.Label(txt_subframe, text=f"{pet.breed} • {pet.age} y.o.", font=("Segoe UI", 9),
                 fg=self.colors["text_gray"], bg="white").pack(anchor="w")

        btns_frame = tk.Frame(card, bg="white")
        btns_frame.pack(side=tk.RIGHT)

        tk.Button(btns_frame, text="VIEW", font=("Segoe UI", 8, "bold"), fg=self.colors["accent"],
                  bg="white", relief=tk.FLAT, cursor="hand2",
                  command=lambda p=pet: self.show_details(p)).pack(side=tk.TOP)

        tk.Button(btns_frame, text="DELETE", font=("Segoe UI", 7), fg="#E74C3C",
                  bg="white", relief=tk.FLAT, cursor="hand2",
                  command=lambda i=index: self.remove_pet(i)).pack(side=tk.TOP)

    @handle_error
    def add_pet_window(self, pet_type):
        win = tk.Toplevel(self.window)
        win.title(f"Add {pet_type}")
        win.geometry("340x600")
        win.configure(bg="white")
        win.grab_set()

        color = self.colors["primary"] if pet_type == "Dog" else self.colors["secondary_b"]
        tk.Label(win, text=f"NEW {pet_type.upper()}", font=("Segoe UI", 14, "bold"),
                 fg="white", bg=color, pady=20).pack(fill=tk.X)

        fields = [("Name", "Buddy"), ("Age", "2"), ("Weight", "5.5"), ("Breed", "Golden"), ("Character", "Playful")]
        entries = {}
        form = tk.Frame(win, bg="white", padx=30, pady=20)
        form.pack(fill=tk.BOTH)

        for label, _ in fields:
            tk.Label(form, text=label.upper(), font=("Segoe UI", 8, "bold"), fg=self.colors["text_gray"],
                     bg="white").pack(anchor="w", pady=(10, 0))
            e = tk.Entry(form, bg="#F4F7F6", relief=tk.FLAT, font=("Segoe UI", 10))
            e.pack(fill=tk.X, ipady=8)
            entries[label] = e

        def submit():
            try:
                cls = Dog if pet_type == "Dog" else Cat
                new_pet = cls(entries["Name"].get(), int(entries["Age"].get()),
                              float(entries["Weight"].get()), entries["Breed"].get(), entries["Character"].get())
                self.pets.append(new_pet)
                self.save_pets()
                self.refresh_list()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Age/Weight must be numbers")

        tk.Button(win, text="SAVE PET", bg=self.colors["accent"], fg="white",
                  font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=submit, pady=12).pack(fill=tk.X, padx=30,
                                                                                               pady=20)

    def load_pets(self):
        if not os.path.exists("pets_data.json"): return []
        try:
            with open("pets_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                p_type = item.pop("type", "Dog")
                cls = Dog if p_type == "Dog" else Cat
                loaded.append(cls(**item))
            return loaded
        except Exception:
            return []

    def save_pets(self):
        data = [p.to_dict() for p in self.pets]
        with open("pets_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def remove_pet(self, index):
        if messagebox.askyesno("Delete", f"Remove {self.pets[index].name}?"):
            self.pets.pop(index)
            self.save_pets()
            self.refresh_list()

    def show_details(self, pet):
        profile = tk.Toplevel(self.window)
        profile.geometry("340x600")
        profile.configure(bg="#F4F7F6")
        color = self.colors["primary"] if isinstance(pet, Dog) else self.colors["secondary_b"]

        header = tk.Frame(profile, bg=color, pady=30)
        header.pack(fill=tk.X)
        tk.Label(header, text=pet.name.upper(), font=("Segoe UI", 18, "bold"), fg="white", bg=color).pack()
        tk.Label(header, text="Health Profile", font=("Segoe UI", 9), fg="white", bg=color).pack()

        body = tk.Frame(profile, bg="#F4F7F6", padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        data_card = tk.Frame(body, bg="white", padx=15, pady=15)
        data_card.pack(fill=tk.X)

        details = [("Breed", pet.breed), ("Age", f"{pet.age} years"),
                   ("Weight", f"{pet.weight} kg"), ("Diet", f"{pet.calculate_daily_calories():.0f} kcal")]

        for lbl, val in details:
            row = tk.Frame(data_card, bg="white", pady=5)
            row.pack(fill=tk.X)
            tk.Label(row, text=lbl, bg="white", fg=self.colors["text_gray"], font=("Segoe UI", 9)).pack(side=tk.LEFT)
            tk.Label(row, text=val, bg="white", fg=self.colors["secondary_b"], font=("Segoe UI", 9, "bold")).pack(
                side=tk.RIGHT)
            tk.Frame(data_card, bg="#F4F7F6", height=1).pack(fill=tk.X, pady=5)

        tk.Button(profile, text="BACK", bg=self.colors["secondary_b"], fg="white",
                  relief=tk.FLAT, font=("Segoe UI", 9, "bold"), command=profile.destroy, pady=10).pack(fill=tk.X,
                                                                                                       padx=20, pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()