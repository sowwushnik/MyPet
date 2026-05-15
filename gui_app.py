import tkinter as tk
from tkinter import messagebox, ttk
from models import Dog, Cat
import json
import os


class PetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyPet Health Tracker Pro")
        self.root.geometry("900x650")
        self.root.configure(bg="#F4F7F6")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="white",
                             fieldbackground="white",
                             rowheight=35,
                             font=("Segoe UI", 10),
                             borderwidth=0)
        self.style.configure("Treeview.Heading",
                             font=("Segoe UI", 11, "bold"),
                             background="#ECF0F1",
                             foreground="#2C3E50",
                             relief="flat")
        self.style.map("Treeview", background=[('selected', '#3498DB')])

        self.pets = self.load_pets()

        header = tk.Frame(root, bg="#2C3E50", height=80)
        header.pack(fill=tk.X)

        tk.Label(header, text="MYPET MANAGEMENT SYSTEM",
                 font=("Segoe UI", 22, "bold"), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        container = tk.Frame(root, bg="#F4F7F6")
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        table_border = tk.Frame(container, bg="#D5D8DC", bd=1)
        table_border.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_border, columns=("Name", "Type", "Age", "Status"), show="headings")
        for col in ("Name", "Type", "Age", "Status"):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.btn_frame = tk.Frame(root, bg="#F4F7F6")
        self.btn_frame.pack(pady=30)

        self.add_styled_buttons()
        self.refresh_list()

    def add_styled_buttons(self):
        buttons = [
            ("ADD DOG", "#27AE60", lambda: self.add_pet_window("Dog")),
            ("ADD CAT", "#8E44AD", lambda: self.add_pet_window("Cat")),
            ("VIEW PROFILE", "#2980B9", self.show_details),
            ("REMOVE", "#E74C3C", self.remove_pet),
            ("SAVE & EXIT", "#34495E", self.save_and_exit)
        ]

        for i, (text, color, cmd) in enumerate(buttons):
            btn = tk.Button(self.btn_frame, text=text, bg=color, fg="white",
                            font=("Segoe UI", 10, "bold"), width=15, height=2,
                            relief=tk.FLAT, cursor="hand2", command=cmd)
            btn.grid(row=0, column=i, padx=10)

            btn.bind("<Enter>", lambda e, b=btn, c=color: b.configure(bg=self.adjust_color(c, 20)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))

        self.refresh_list()

    def adjust_color(self, hex_color, amount):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        new_rgb = tuple(min(255, c + amount) for c in rgb)
        return "#%02x%02x%02x" % new_rgb

    def load_pets(self):
        filename = "pets_data.json"
        if not os.path.exists(filename): return []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                if item["type"] == "Dog":
                    p = Dog(item["name"], item["age"], item["weight"], item["breed"], item["temperament"])
                else:
                    p = Cat(item["name"], item["age"], item["weight"], item["breed"], item["temperament"])
                p.is_vaccinated = item.get("is_vaccinated", False)
                p.last_checkup = item.get("last_checkup", "Not recorded")
                p.health_logs = item.get("health_logs", [])
                loaded.append(p)
            return loaded
        except:
            return []

    def save_and_exit(self):
        data = [p.to_dict() for p in self.pets]
        with open("pets_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        self.root.destroy()

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.pets:
            self.tree.insert("", tk.END, values=(p.name, p.__class__.__name__, f"{p.age}y", p.check_health_status()))

    def add_pet_window(self, pet_type):
        win = tk.Toplevel(self.root)
        win.title(f"New {pet_type} Registration")
        win.geometry("350x500")
        win.configure(bg="white")
        win.grab_set()

        tk.Label(win, text=f"REGISTER {pet_type.upper()}",
                 font=("Segoe UI", 14, "bold"), bg="white", fg="#2C3E50").pack(pady=20)

        fields = ["Name", "Age", "Weight", "Breed", "Character"]
        entries = {}

        for field in fields:
            lbl = tk.Label(win, text=field, font=("Segoe UI", 9, "bold"), bg="white", fg="#7F8C8D")
            lbl.pack(anchor="w", padx=40)

            entry = tk.Entry(win, font=("Segoe UI", 10), bg="#F4F7F6", relief=tk.FLAT, bd=8)
            entry.pack(fill=tk.X, padx=40, pady=(0, 10))
            entries[field] = entry

        entries["Name"].focus_set()

        def submit():
            try:
                name = entries["Name"].get().strip()
                if not name:
                    messagebox.showerror("Error", "Name is required!")
                    return

                age = int(entries["Age"].get())
                weight = float(entries["Weight"].get())
                breed = entries["Breed"].get()
                temp = entries["Character"].get()

                new_pet = Dog(name, age, weight, breed, temp) if pet_type == "Dog" else Cat(name, age, weight, breed,
                                                                                            temp)

                self.pets.append(new_pet)
                self.refresh_list()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Age and Weight must be numbers!")

        btn_save = tk.Button(win, text="CONFIRM", bg="#27AE60", fg="white",
                             font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                             cursor="hand2", command=submit)
        btn_save.pack(fill=tk.X, padx=40, pady=30)

    def show_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a pet to view their profile!")
            return

        index = self.tree.index(selected[0])
        pet = self.pets[index]

        profile_win = tk.Toplevel(self.root)
        profile_win.title(f"Pet Profile: {pet.name}")
        profile_win.geometry("400x550")
        profile_win.configure(bg="white")
        profile_win.grab_set()

        header_color = "#27AE60" if pet.__class__.__name__ == "Dog" else "#8E44AD"
        top_bar = tk.Frame(profile_win, bg=header_color, height=100)
        top_bar.pack(fill=tk.X)

        tk.Label(top_bar, text=pet.name.upper(), font=("Segoe UI", 20, "bold"),
                 fg="white", bg=header_color).pack(pady=25)

        info_frame = tk.Frame(profile_win, bg="white")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        def add_info_row(label, value, color="#2C3E50"):
            row = tk.Frame(info_frame, bg="white")
            row.pack(fill=tk.X, pady=8)
            tk.Label(row, text=label, font=("Segoe UI", 10, "bold"),
                     fg="#7F8C8D", bg="white").pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Segoe UI", 11),
                     fg=color, bg="white").pack(side=tk.RIGHT)
            line = tk.Frame(info_frame, bg="#F4F7F6", height=1)
            line.pack(fill=tk.X)

        status_color = "#27AE60"
        if "Overweight" in pet.check_health_status() or "Underweight" in pet.check_health_status():
            status_color = "#E67E22"
        elif "Senior" in pet.check_health_status():
            status_color = "#2980B9"


        add_info_row("TYPE", pet.__class__.__name__)
        add_info_row("BREED", pet.breed)
        add_info_row("AGE", f"{pet.age} years")
        add_info_row("WEIGHT", f"{pet.weight} kg")
        add_info_row("CALORIES", f"{pet.calculate_daily_calories():.1f} kcal")
        add_info_row("VACCINATION", pet.get_vaccination_status(),
                     color="#27AE60" if pet.is_vaccinated else "#E74C3C")

        status_frame = tk.Frame(info_frame, bg="#FDFEFE", bd=1, relief=tk.SOLID)
        status_frame.pack(fill=tk.X, pady=20)
        tk.Label(status_frame, text="HEALTH ANALYSIS", font=("Segoe UI", 8, "bold"),
                 bg="#FDFEFE", fg="#BDC3C7").pack(pady=(5, 0))
        tk.Label(status_frame, text=pet.check_health_status(), font=("Segoe UI", 10, "bold"),
                 bg="#FDFEFE", fg=status_color, wraplength=300).pack(pady=10)

        tk.Button(profile_win, text="CLOSE", font=("Segoe UI", 10, "bold"),
                  bg="#34495E", fg="white", relief=tk.FLAT, cursor="hand2",
                  command=profile_win.destroy).pack(pady=20, padx=30, fill=tk.X)

    def remove_pet(self):
        selected = self.tree.selection()
        if not selected: return

        index = self.tree.index(selected[0])
        if messagebox.askyesno("Confirm", f"Delete {self.pets[index].name}?"):
            self.pets.pop(index)
            self.refresh_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = PetApp(root)
    root.mainloop()