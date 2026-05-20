import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from utils.config import THEME


class DailyLogWindow:
    def __init__(self, parent_window, pet, storage, parent_root=None):
        self.window = tk.Toplevel(parent_window)
        self.pet = pet
        self.storage = storage
        self.parent_root = parent_root

        self.window.title(f"Daily Log — {self.pet.name}")
        self.window.geometry("360x700")
        self.window.configure(bg=THEME["bg"])

        self.window.transient(parent_window)
        self.window.grab_set()

        header = tk.Frame(self.window, bg=THEME["primary"], padx=20, pady=20)
        header.pack(fill=tk.X)

        tk.Label(header, text="DAILY LOG", font=("Segoe UI", 14, "bold"), fg="white", bg=THEME["primary"]).pack(
            side=tk.LEFT)
        tk.Label(header, text=f"🐾 {self.pet.name}", font=("Segoe UI", 10, "bold"), fg="white",
                 bg=THEME["primary"]).pack(side=tk.RIGHT, pady=3)

        nav_frame = tk.Frame(self.window, bg=THEME["white"])
        nav_frame.pack(fill=tk.X)

        self.btn_form_tab = tk.Button(nav_frame, text="➕ New Entry", font=("Segoe UI", 9, "bold"),
                                      bg=THEME["white"], fg=THEME["primary"], bd=0, relief=tk.FLAT, pady=10,
                                      command=self.switch_to_form)
        self.btn_form_tab.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_history_tab = tk.Button(nav_frame, text="📜 History", font=("Segoe UI", 9),
                                         bg="#F2F4F4", fg=THEME["text_gray"], bd=0, relief=tk.FLAT, pady=10,
                                         command=self.switch_to_history)
        self.btn_history_tab.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        self.content_frame = tk.Frame(self.window, bg=THEME["bg"])
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.food_amount = tk.StringVar(value="100")
        self.water_drank = tk.StringVar(value="200")
        self.mood_var = tk.StringVar(value="😊 Happy")
        self.poop_var = tk.StringVar(value="✅ Normal")

        self.switch_to_form()

    def create_scrollable_area(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.content_frame, bg=THEME["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg=THEME["bg"])

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=340)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.window.bind("<Configure>", self._on_window_resize)
        self.window.bind("<Enter>", self._bind_mousewheel)
        self.window.bind("<Leave>", self._unbind_mousewheel)

    def switch_to_form(self):
        self.btn_form_tab.configure(bg=THEME["white"], fg=THEME["primary"], font=("Segoe UI", 9, "bold"))
        self.btn_history_tab.configure(bg="#F2F4F4", fg=THEME["text_gray"], font=("Segoe UI", 9))
        self.create_scrollable_area()
        self.render_form()

    def switch_to_history(self):
        self.btn_history_tab.configure(bg=THEME["white"], fg=THEME["primary"], font=("Segoe UI", 9, "bold"))
        self.btn_form_tab.configure(bg="#F2F4F4", fg=THEME["text_gray"], font=("Segoe UI", 9))
        self.create_scrollable_area()
        self.render_history()

    def _on_window_resize(self, event):
        if hasattr(self, 'canvas') and hasattr(self, 'canvas_window'):
            canvas_width = self.canvas.winfo_width()
            if canvas_width > 10:
                self.canvas.itemconfigure(self.canvas_window, width=canvas_width - 5)

    def _on_mousewheel(self, event):
        if hasattr(self, 'canvas'):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_mousewheel(self, event):
        self.window.bind_all("<MouseWheel>", self._on_mousewheel)
        self.window.bind_all("<Button-4>", self._on_mousewheel)
        self.window.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.window.unbind_all("<MouseWheel>")
        self.window.unbind_all("<Button-4>")
        self.window.unbind_all("<Button-5>")

    def render_form(self):
        food_card = tk.Frame(self.scroll_frame, bg="white", padx=15, pady=15, highlightbackground="#EBF0F1",
                             highlightthickness=1)
        food_card.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(food_card, text="🥩 NUTRITION & HYDRATION", font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                 bg="white").pack(anchor="w", pady=(0, 10))

        tk.Label(food_card, text="Food Served (grams)", font=("Segoe UI", 9, "bold"), fg=THEME["secondary_b"],
                 bg="white").pack(anchor="w")
        e_food = tk.Entry(food_card, textvariable=self.food_amount, bg=THEME["bg"], relief=tk.FLAT,
                          font=("Segoe UI", 10))
        e_food.pack(fill=tk.X, ipady=6, pady=(2, 10))

        tk.Label(food_card, text="Water Intake (ml)", font=("Segoe UI", 9, "bold"), fg=THEME["secondary_b"],
                 bg="white").pack(anchor="w")
        e_water = tk.Entry(food_card, textvariable=self.water_drank, bg=THEME["bg"], relief=tk.FLAT,
                           font=("Segoe UI", 10))
        e_water.pack(fill=tk.X, ipady=6, pady=(2, 0))

        status_card = tk.Frame(self.scroll_frame, bg="white", padx=15, pady=15, highlightbackground="#EBF0F1",
                             highlightthickness=1)
        status_card.pack(fill=tk.X, pady=10, padx=5)

        tk.Label(status_card, text="🎭 MOOD & WELLBEING", font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                 bg="white").pack(anchor="w", pady=(0, 10))

        tk.Label(status_card, text="Pet's Mood Today", font=("Segoe UI", 9, "bold"), fg=THEME["secondary_b"],
                 bg="white").pack(anchor="w")
        mood_combo = ttk.Combobox(status_card, textvariable=self.mood_var,
                                  values=["😊 Happy", "😴 Sleepy", "🦊 Energetic", "😟 Anxious", "🤒 Lethargic"],
                                  state="readonly")
        mood_combo.pack(fill=tk.X, pady=(2, 12))

        tk.Label(status_card, text="Stool / Digestion Status", font=("Segoe UI", 9, "bold"), fg=THEME["secondary_b"],
                 bg="white").pack(anchor="w")
        poop_combo = ttk.Combobox(status_card, textvariable=self.poop_var,
                                  values=["✅ Normal", "❌ Diarrhea", "🪵 Constipated", "⚠️ Unusual Color"],
                                  state="readonly")
        poop_combo.pack(fill=tk.X, pady=(2, 0))

        notes_card = tk.Frame(self.scroll_frame, bg="white", padx=15, pady=15, highlightbackground="#EBF0F1",
                              highlightthickness=1)
        notes_card.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(notes_card, text="📝 ADDITIONAL NOTES", font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                 bg="white").pack(anchor="w", pady=(0, 5))
        self.notes_text = tk.Text(notes_card, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 9), height=4,
                                  wrap=tk.WORD)
        self.notes_text.pack(fill=tk.BOTH, pady=5)

        btn_save = tk.Button(self.scroll_frame, text="💾 SAVE DAILY LOG", bg=THEME["accent"], fg="white",
                             font=("Segoe UI", 10, "bold"), relief=tk.FLAT, pady=12, command=self.save_log)
        btn_save.pack(fill=tk.X, pady=20, padx=5)

    def render_history(self):
        logs = getattr(self.pet, 'daily_logs', []) or []

        if not logs:
            empty_card = tk.Frame(self.scroll_frame, bg="white", padx=15, pady=25,
                                  highlightbackground="#EBF0F1", highlightthickness=1)
            empty_card.pack(fill=tk.X, pady=15, padx=5)
            tk.Label(empty_card, text="📭 No daily logs recorded yet.", font=("Segoe UI", 10, "bold"),
                     fg=THEME["text_gray"], bg="white").pack()
            tk.Label(empty_card, text="Use 'New Entry' tab to log your pet's status.", font=("Segoe UI", 8),
                     fg=THEME["text_gray"], bg="white").pack(pady=(5, 0))
            return

        for log in reversed(logs):
            card = tk.Frame(self.scroll_frame, bg="white", padx=15, pady=12,
                            highlightbackground="#EBF0F1", highlightthickness=1)
            card.pack(fill=tk.X, pady=5, padx=5)

            tk.Label(card, text=log.get("timestamp", "Date N/A"), font=("Segoe UI", 9, "bold"),
                     fg=THEME["primary"], bg="white").pack(anchor="w")

            grid_frame = tk.Frame(card, bg="white", pady=5)
            grid_frame.pack(fill=tk.X)

            tk.Label(grid_frame, text=f"🥩 Food: {log.get('food_g', 0)}g   💧 Water: {log.get('water_ml', 0)}ml",
                     font=("Segoe UI", 9), fg=THEME["secondary_b"], bg="white").pack(anchor="w", pady=1)
            tk.Label(grid_frame, text=f"🎭 Mood: {log.get('mood', 'N/A')}",
                     font=("Segoe UI", 9), fg=THEME["secondary_b"], bg="white").pack(anchor="w", pady=1)
            tk.Label(grid_frame, text=f"💩 Digestion: {log.get('digestion', 'N/A')}",
                     font=("Segoe UI", 9), fg=THEME["secondary_b"], bg="white").pack(anchor="w", pady=1)

            if log.get("notes"):
                tk.Frame(card, height=1, bg="#F2F4F4").pack(fill=tk.X, pady=6)
                tk.Label(card, text=log["notes"], font=("Segoe UI", 9, "italic"),
                         fg=THEME["text_gray"], bg="white", wraplength=290, justify="left").pack(anchor="w")

    def save_log(self):
        try:
            food = float(self.food_amount.get().strip())
            water = float(self.water_drank.get().strip())
        except ValueError:
            messagebox.showerror("Validation Error", "Please provide numeric values for food and water intake.")
            return

        notes = self.notes_text.get("1.0", tk.END).strip()

        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "food_g": food,
            "water_ml": water,
            "mood": self.mood_var.get(),
            "digestion": self.poop_var.get(),
            "notes": notes
        }

        if not hasattr(self.pet, 'daily_logs'):
            self.pet.daily_logs = []

        self.pet.daily_logs.append(log_entry)

        all_pets = self.storage.load_pets()

        found = False
        for idx, saved_pet in enumerate(all_pets):
            if saved_pet.name == self.pet.name:
                all_pets[idx] = self.pet
                found = True
                break

        if not found:
            all_pets.append(self.pet)

        self.storage.save_pets(all_pets)

        messagebox.showinfo("Success", f"Daily log for {self.pet.name} saved successfully! 🎉")

        if self.parent_root:
            self.parent_root.event_generate("<<PetDataChanged>>")

        self.switch_to_history()