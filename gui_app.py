import tkinter as tk
from tkinter import messagebox, ttk
from utils.decorators import handle_error
from config import THEME, PET_CLASSES


class MainMenu:
    def __init__(self, root, storage):
        self.root = root
        self.storage = storage

        self.root.title("MyPet Pro")
        self.root.geometry("360x700")
        self.root.configure(bg=THEME["bg"])

        header = tk.Frame(self.root, bg=THEME["teal"], padx=20, pady=30)
        header.pack(fill=tk.X)

        tk.Label(header, text="Good morning, Meirkhan!", font=("Segoe UI", 18, "bold"),
                 fg="white", bg=THEME["teal"]).pack(anchor="w")
        tk.Label(header, text="Everything is under control 🐾", font=("Segoe UI", 10),
                 fg="white", bg=THEME["teal"]).pack(anchor="w")

        avatar_frame = tk.Frame(header, bg=THEME["teal"], pady=15)
        avatar_frame.pack(fill=tk.X)
        for icon in ["🐕", "🐈"]:
            tk.Label(avatar_frame, text=icon, font=("Segoe UI", 18), bg=THEME["teal"], fg="white", width=2).pack(
                side=tk.LEFT, padx=5)

        body = tk.Frame(self.root, bg=THEME["bg"], padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        tk.Label(body, text="QUICK NAVIGATION", font=("Segoe UI", 8, "bold"),
                 fg="#95A5A6", bg=THEME["bg"]).pack(anchor="w", pady=(0, 10))

        self.add_mobile_card(body, "🐕 MY PETS", "Database & Profiles", THEME["secondary_b"], self.open_database)
        self.add_mobile_card(body, "📊 HEALTH", "Weight & Activity", THEME["teal"],
                             lambda: messagebox.showinfo("Info", "Health module coming soon!"))
        self.add_mobile_card(body, "🚪 EXIT", "Close Application", "#7F8C8D", self.root.quit)

        nav_bar = tk.Frame(self.root, bg=THEME["white"], height=60, highlightbackground="#ECF0F1", highlightthickness=1)
        nav_bar.pack(fill=tk.X, side=tk.BOTTOM)
        for icon, name in [("🏠", "Home"), ("🏥", "Health"), ("🔔", "Reminders"), ("🐾", "Profile")]:
            btn = tk.Frame(nav_bar, bg=THEME["white"])
            btn.pack(side=tk.LEFT, expand=True)
            tk.Label(btn, text=icon, font=("Segoe UI", 14), bg=THEME["white"]).pack()
            tk.Label(btn, text=name, font=("Segoe UI", 7), bg=THEME["white"], fg=THEME["text_gray"]).pack()

    def add_mobile_card(self, master, title, sub, color, command):
        card = tk.Frame(master, bg="white", cursor="hand2", pady=15, padx=15)
        card.pack(fill=tk.X, pady=8)
        tk.Frame(card, bg=color, width=4).pack(side=tk.LEFT, fill=tk.Y)

        txt_frame = tk.Frame(card, bg="white", padx=10)
        txt_frame.pack(side=tk.LEFT)

        tk.Label(txt_frame, text=title, font=("Segoe UI", 11, "bold"), fg=color, bg=THEME["white"]).pack(anchor="w")
        tk.Label(txt_frame, text=sub, font=("Segoe UI", 9), fg=THEME["text_gray"], bg=THEME["white"]).pack(anchor="w")

        def on_click(e): command()

        card.bind("<Button-1>", on_click)
        for child in card.winfo_children():
            child.bind("<Button-1>", on_click)

    def open_database(self):
        PetApp(tk.Toplevel(self.root), self.storage)


class PetApp:
    def __init__(self, window, storage):
        self.window = window
        self.storage = storage

        self.window.title("My Pets")
        self.window.geometry("360x700")
        self.window.configure(bg=THEME["bg"])
        self.window.grab_set()

        header = tk.Frame(self.window, bg=THEME["secondary_b"], padx=20, pady=25)
        header.pack(fill=tk.X)

        tk.Label(header, text="MY PETS", font=("Segoe UI", 16, "bold"), fg="white", bg=THEME["secondary_b"]).pack(
            side=tk.LEFT)

        tk.Button(header, text="✕", font=("Segoe UI", 12, "bold"), fg="white", bg=THEME["secondary_b"], relief=tk.FLAT,
                  cursor="hand2",
                  command=self.window.destroy).pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self.window, bg=THEME["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=THEME["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=340)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.pets = self.storage.load_pets()
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.pets:
            tk.Label(self.scrollable_frame, text="No pets registered yet",
                     bg="#F4F7F6", fg=THEME["text_gray"], pady=50).pack(pady=50)
        else:
            for idx, pet in enumerate(self.pets):
                self.add_pet_card(pet, idx)

        tk.Button(self.scrollable_frame, text="ADD PET", bg=THEME["primary"], fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, pady=12, cursor="hand2", command=self.add_pet_window).pack(fill=tk.X, pady=20, padx=5)

    def add_pet_card(self, pet, index):
        card = tk.Frame(self.scrollable_frame, bg=THEME["white"], pady=15, padx=15)
        card.pack(fill=tk.X, pady=8)

        card.bind("<Enter>", lambda e: card.configure(bg="#F9F9F9"))
        card.bind("<Leave>", lambda e: card.configure(bg=THEME["white"]))

        icon = "🐕" if pet.__class__.__name__ == "Dog" else "🐈"
        info_frame = tk.Frame(card, bg=THEME["white"])
        info_frame.pack(side=tk.LEFT)

        tk.Label(info_frame, text=icon, font=("Segoe UI", 24), bg=THEME["white"]).pack(side=tk.LEFT, padx=(0, 10))

        txt_subframe = tk.Frame(info_frame, bg=THEME["white"])
        txt_subframe.pack(side=tk.LEFT)

        name_row = tk.Frame(txt_subframe, bg=THEME["white"])
        name_row.pack(anchor="w")

        tk.Label(name_row, text=pet.name.upper(), font=("Segoe UI", 11, "bold"),
                 fg=THEME["secondary_b"], bg=THEME["white"]).pack(side=tk.LEFT)

        if getattr(pet, "is_vaccinated", False):
            tk.Label(name_row, text="🛡️", font=("Segoe UI", 9), bg=THEME["white"], fg=THEME["teal"]).pack(side=tk.LEFT,
                                                                                                          padx=5)

        tk.Label(txt_subframe, text=f"{pet.breed} • {pet.age} y.o.", font=("Segoe UI", 9), fg=THEME["text_gray"],
                 bg=THEME["white"]).pack(anchor="w")

        btns_frame = tk.Frame(card, bg=THEME["white"])
        btns_frame.pack(side=tk.RIGHT)

        tk.Button(btns_frame, text="VIEW", font=("Segoe UI", 8, "bold"), fg=THEME["accent"],
                  bg=THEME["white"], relief=tk.FLAT, cursor="hand2",
                  command=lambda p=pet: self.show_details(p)).pack(side=tk.TOP)

        tk.Button(btns_frame, text="DELETE", font=("Segoe UI", 7), fg=THEME["danger"],
                  bg=THEME["white"], relief=tk.FLAT, cursor="hand2",
                  command=lambda i=index: self.remove_pet(i)).pack(side=tk.TOP)

    @handle_error
    def add_pet_window(self):
        win = tk.Toplevel(self.window)
        win.geometry("340x600")
        win.configure(bg=THEME["white"])
        win.grab_set()
        win.focus_set()

        tk.Label(win, text="NEW PET PROFILE", bg=THEME["primary"], fg="white", font=("Segoe UI", 14, "bold"),
                 pady=20).pack(fill=tk.X)

        form = tk.Frame(win, bg=THEME["white"], padx=30, pady=20)
        form.pack(fill=tk.BOTH)

        pet_type_var = tk.StringVar(value="Dog")
        ttk.Combobox(form, textvariable=pet_type_var, values=["Dog", "Cat"], state="readonly").pack(fill=tk.X,
                                                                                                    pady=(0, 15))

        fields = [("Name", "Buddy"), ("Age", "1"), ("Weight", "5.0"), ("Breed", "Poodle"), ("Character", "Calm")]
        entries = {}

        for label, placeholder in fields:
            tk.Label(form, text=label.upper(), bg=THEME["white"], fg=THEME["text_gray"],
                     font=("Segoe UI", 8, "bold")).pack(
                anchor="w", padx=30, pady=(10, 0))
            e = tk.Entry(form, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 10))
            e.insert(0, placeholder)
            e.pack(fill=tk.X, ipady=8)
            entries[label] = e

        self.vaccine_var = tk.BooleanVar(value=False)
        tk.Checkbutton(form, text="IS VACCINATED", variable=self.vaccine_var,
                       font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                       bg=THEME["white"], activebackground=THEME["white"]).pack(anchor="w", pady=10)

        def submit():
            name = entries["Name"].get().strip()
            age_raw = entries["Age"].get().strip()
            weight_raw = entries["Weight"].get().strip()

            if not name:
                messagebox.showwarning("Validation error", "Name cannot be empty")
                return

            try:
                age = int(age_raw)
                weight = float(weight_raw)
                if age < 0 or weight <= 0: raise ValueError
            except ValueError:
                messagebox.showwarning("Validation error", "Age must be an integer and Weight must be positive")
                return

            cls = PET_CLASSES.get(pet_type_var.get())
            new_pet = cls(
                name=name,
                age=age,
                weight=weight,
                breed=entries["Breed"].get().strip() or "Unknown",
                temperament=entries["Character"].get().strip() or "Unknown",
                is_vaccinated=self.vaccine_var.get()
            )

            self.pets.append(new_pet)
            self.storage.save_pets(self.pets)
            self.refresh_list()
            win.destroy()

        tk.Button(win, text="SAVE PET", bg=THEME["accent"], fg="white",
                  font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=submit, pady=12).pack(fill=tk.X, padx=30,
                                                                                               pady=20)

    def show_details(self, pet):
        profile = tk.Toplevel(self.window)
        profile.geometry("340x750")
        profile.configure(bg=THEME["bg"])
        profile.grab_set()

        color = THEME["primary"] if pet.__class__.__name__ == "Dog" else THEME["secondary_b"]

        header = tk.Frame(profile, bg=color, pady=30)
        header.pack(fill=tk.X)
        tk.Label(header, text=pet.name.upper(), font=("Segoe UI", 18, "bold"), fg="white", bg=color).pack()

        body = tk.Frame(profile, bg=THEME["bg"], padx=20, pady=10)
        body.pack(fill=tk.BOTH, expand=True)

        info_card = tk.Frame(body, bg=THEME["white"], padx=15, pady=15)
        info_card.pack(fill=tk.X, pady=(0, 15))

        stats = [
            ("Breed:", pet.breed),
            ("Age:", f"{pet.age} yrs"),
            ("Weight:", f"{pet.weight} kg"),
            ("Status:", "Vaccinated 🛡️" if pet.is_vaccinated else "No vaccine")
        ]

        for label, value in stats:
            row = tk.Frame(info_card, bg=THEME["white"])
            row.pack(fill=tk.X, pady=2)
            tk.Label(row, text=label, font=("Segoe UI", 9), fg="gray", bg=THEME["white"]).pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Segoe UI", 9, "bold"), bg=THEME["white"]).pack(side=tk.RIGHT)

        tk.Label(body, text="HEALTH LOGS", font=("Segoe UI", 8, "bold"), fg="gray", bg=THEME["bg"]).pack(anchor="w")

        log_frame = tk.Frame(body, bg=THEME["white"], padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        lb = tk.Listbox(log_frame, font=("Segoe UI", 9), relief=tk.FLAT, height=8, bg=THEME["white"],
                        highlightthickness=0)
        lb.pack(fill=tk.BOTH, expand=True)
        for log in pet.health_logs:
            lb.insert(tk.END, log)

        entry = tk.Entry(log_frame, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 9))
        entry.insert(0, "Enter medical note...")
        entry.pack(fill=tk.X, pady=(10, 5), ipady=5)

        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == "Enter medical note..." else None)
        entry.bind("<FocusOut>", lambda e: entry.insert(0, "Enter medical note...") if not entry.get() else None)

        def add_log():
            note = entry.get().strip()
            if note and note != "Enter medical note...":
                pet.add_log(note)
                lb.insert(tk.END, pet.health_logs[-1])
                lb.yview(tk.END)
                entry.delete(0, tk.END)
                self.storage.save_pets(self.pets)

        tk.Button(log_frame, text="ADD NOTE", bg=THEME["accent"], fg="white",
                  relief=tk.FLAT, font=("Segoe UI", 9, "bold"), command=add_log).pack(fill=tk.X)

        footer = tk.Frame(profile, bg=THEME["bg"], pady=15)
        footer.pack(fill=tk.X, side=tk.BOTTOM)

        tk.Button(footer, text="EDIT PROFILE", bg=THEME["teal"], fg="white",
                  relief=tk.FLAT, width=15, command=lambda: self.edit_pet_window(pet, profile)).pack(side=tk.LEFT,
                                                                                                     padx=20)

        tk.Button(footer, text="CLOSE", bg="#BDC3C7", fg="white",
                  relief=tk.FLAT, width=10, command=profile.destroy).pack(side=tk.RIGHT, padx=20)

    def edit_pet_window(self, pet, profile_win):
        profile_win.destroy()

        win = tk.Toplevel(self.window)
        win.title(f"Edit {pet.name}")
        win.geometry("340x600")
        win.configure(bg=THEME["white"])
        win.grab_set()
        win.focus_set()

        tk.Label(win, text="EDIT PROFILE", font=("Segoe UI", 14, "bold"), fg="white", bg=THEME["accent"],
                 pady=20).pack(fill=tk.X)

        form = tk.Frame(win, bg=THEME["white"], padx=30, pady=20)
        form.pack(fill=tk.X)

        fields = [("Name", pet.name),
                  ("Age", str(pet.age)),
                  ("Weight", str(pet.weight)),
                  ("Breed", pet.breed),
                  ("Character", pet.temperament)]
        entries = {}

        for label, value in fields:
            tk.Label(form, text=label.upper(), font=("Segoe UI", 8, "bold"),
                     fg=THEME["text_gray"], bg=THEME["white"]).pack(anchor="w", pady=(10, 0))
            e = tk.Entry(form, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 10))
            e.insert(0, value)
            e.pack(fill=tk.X, ipady=8)
            entries[label] = e

        self.edit_vaccine_var = tk.BooleanVar(value=getattr(pet, "is_vaccinated", False))
        tk.Checkbutton(form, text="IS VACCINATED", variable=self.edit_vaccine_var,
                       font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"], bg=THEME["white"],
                       activebackground=THEME["white"]).pack(anchor="w", pady=10)

        def update():
            try:
                pet.name = entries["Name"].get().strip()
                pet.age = int(entries["Age"].get())
                pet.weight = float(entries["Weight"].get())
                pet.breed = entries["Breed"].get().strip()
                pet.temperament = entries["Character"].get().strip()
                pet.is_vaccinated = self.edit_vaccine_var.get()

                self.storage.save_pets(self.pets)
                self.refresh_list()
                win.destroy()
                messagebox.showinfo("Success", f"Profile for {pet.name} updated!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values for Age and Weight")

        tk.Button(win, text="SAVE CHANGES", bg=THEME["accent"], fg="white",
                  font=("Segoe UI", 10, "bold"), relief=tk.FLAT, command=update, pady=12).pack(fill=tk.X, padx=30,
                                                                                               pady=20)

    def remove_pet(self, index):
        if messagebox.askyesno("Delete", f"Remove {self.pets[index].name}?"):
            self.pets.pop(index)
            self.storage.save_pets(self.pets)
            self.refresh_list()


if __name__ == "__main__":
    from utils.storage import JSONStorage

    root = tk.Tk()
    storage = JSONStorage()
    MainMenu(root, storage)
    root.mainloop()