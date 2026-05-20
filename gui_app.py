import tkinter as tk
from tkinter import messagebox, ttk
from daily_log_window import DailyLogWindow
from utils.decorators import handle_error
from utils.config import THEME, PET_CLASSES


class MainMenu:
    def __init__(self, root, storage):
        self.root = root
        self.storage = storage
        self.pets = self.storage.load_pets()
        self.active_pet = self.pets[0] if self.pets else None

        self.user_profile = {
            "name": "Meirkhan",
            "status": "Student / Pet Lover",
            "notifications": "Enabled"
        }

        self.root.title("MyPet Pro")
        self.root.geometry("360x700")
        self.root.configure(bg=THEME["bg"])

        self.main_container = tk.Frame(self.root, bg=THEME["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.show_home_screen()
        self.render_navbar()

        self.root.bind("<<PetDataChanged>>", lambda e: self.on_pet_data_changed())

    def clear_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def refresh_current_screen(self):
        self.pets = self.storage.load_pets()
        if self.pets and (self.active_pet not in self.pets):
            matching = [p for p in self.pets if p.name == getattr(self.active_pet, 'name', '')]
            self.active_pet = matching[0] if matching else self.pets[0]
        elif not self.pets:
            self.active_pet = None

        if self.current_screen == "Home":
            self.show_home_screen()
        elif self.current_screen == "Health":
            self.show_health_screen()
        elif self.current_screen == "More":
            self.show_more_screen()

    def on_pet_data_changed(self):
        self.refresh_current_screen()

    def show_home_screen(self):
        self.clear_container()
        self.current_screen = "Home"

        header = tk.Frame(self.main_container, bg=THEME["teal"], padx=20, pady=20)
        header.pack(fill=tk.X)

        tk.Label(header, text=f"Good morning, {self.user_profile['name']}!", font=("Segoe UI", 16, "bold"),
                 fg="white", bg=THEME["teal"]).pack(anchor="w")
        tk.Label(header, text="Track your pet's health below 👇", font=("Segoe UI", 9),
                 fg="white", bg=THEME["teal"]).pack(anchor="w", pady=(2, 10))

        self.selector_frame = tk.Frame(header, bg=THEME["teal"])
        self.selector_frame.pack(fill=tk.X, pady=(5, 0))
        self.render_pet_selector()

        self.body = tk.Frame(self.main_container, bg=THEME["bg"], padx=20, pady=15)
        self.body.pack(fill=tk.BOTH, expand=True)
        self.render_dashboard()

    def render_pet_selector(self):
        for widget in self.selector_frame.winfo_children():
            widget.destroy()

        if not self.pets:
            btn = tk.Button(self.selector_frame, text="➕ Add your first pet", bg=THEME["primary"], fg="white",
                            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, command=self.open_my_pet_hub)
            btn.pack(anchor="w")
            return

        for pet in self.pets:
            is_active = (self.active_pet and pet.name == self.active_pet.name)
            icon = "🐕" if pet.__class__.__name__ == "Dog" else "🐈"

            p_btn = tk.Frame(self.selector_frame, bg=THEME["primary"] if is_active else THEME["teal"],
                             highlightbackground="white", highlightthickness=1 if not is_active else 0, padx=8, pady=4)
            p_btn.pack(side=tk.LEFT, padx=5)

            lbl = tk.Label(p_btn, text=f"{icon} {pet.name}", font=("Segoe UI", 9, "bold" if is_active else "normal"),
                           fg="white", bg=THEME["primary"] if is_active else THEME["teal"], cursor="hand2")
            lbl.pack()

            def make_select(selected_pet):
                return lambda e: self.select_pet(selected_pet)

            lbl.bind("<Button-1>", make_select(pet))
            p_btn.bind("<Button-1>", make_select(pet))

    def select_pet(self, pet):
        self.active_pet = pet
        if self.current_screen == "Home":
            self.render_pet_selector()
            self.render_dashboard()
        elif self.current_screen == "Health":
            self.show_health_screen()

    def render_dashboard(self):
        for widget in self.body.winfo_children():
            widget.destroy()

        if not self.active_pet:
            empty_frame = tk.Frame(self.body, bg=THEME["bg"], pady=40)
            empty_frame.pack(fill=tk.BOTH, expand=True)
            tk.Label(empty_frame, text="No pets selected", font=("Segoe UI", 12, "bold"), fg=THEME["text_gray"],
                     bg=THEME["bg"]).pack()
            tk.Button(empty_frame, text="Go to My Pet Hub", bg=THEME["primary"], fg="white", relief=tk.FLAT,
                      command=self.open_my_pet_hub, pady=10).pack(pady=10)
            return

        pet = self.active_pet
        tk.Label(self.body, text=f"{pet.name.upper()}'S QUICK ACTIONS", font=("Segoe UI", 8, "bold"),
                 fg=THEME["text_gray"], bg=THEME["bg"]).pack(anchor="w", pady=(0, 10))

        grid_frame = tk.Frame(self.body, bg=THEME["bg"])
        grid_frame.pack(fill=tk.BOTH, expand=True)

        grid_frame.columnconfigure(0, weight=1, uniform="group1")
        grid_frame.columnconfigure(1, weight=1, uniform="group1")

        self.add_dashboard_tile(grid_frame, 0, 0, "📝", "Daily log", "Routine tracking", THEME["primary"],
                                lambda: self.open_daily_log_module())

        self.add_dashboard_tile(grid_frame, 0, 1, "🩺", "Symptom check", "Health Status", THEME["accent"],
                                lambda: self.show_health_screen(target_tab="care"))

        self.add_dashboard_tile(grid_frame, 1, 0, "🥩", "Feeding", "Meals & Diets", THEME["teal"],
                                lambda: self.show_health_screen(target_tab="care"))

        weight_sub = f"Weight: {pet.weight} kg"
        self.add_dashboard_tile(grid_frame, 1, 1, "⚖️", "Tracker", weight_sub, "#9B59B6",
                                lambda: self.show_health_screen(target_tab="daily"))

    def open_daily_log_module(self):
        if not self.active_pet:
            messagebox.showwarning("No Pet", "Please select or add a pet first before logging!")
            return
        DailyLogWindow(self.root, self.active_pet, self.storage, parent_root=self.root)

    def add_dashboard_tile(self, master, row, col, icon, title, subtitle, color, command):
        card = tk.Frame(master, bg="white", cursor="hand2", padx=12, pady=15,
                        highlightbackground="#ECF0F1", highlightthickness=1)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

        tk.Label(card, text=icon, font=("Segoe UI", 18), bg="white", fg=color).pack(anchor="w")
        tk.Label(card, text=title, font=("Segoe UI", 11, "bold"), fg=THEME["secondary_b"], bg="white").pack(anchor="w",
                                                                                                            pady=(5, 0))
        tk.Label(card, text=subtitle, font=("Segoe UI", 8), fg=THEME["text_gray"], bg="white").pack(anchor="w")

        def on_click(e): command()

        card.bind("<Button-1>", on_click)
        for child in card.winfo_children():
            child.bind("<Button-1>", on_click)

    def show_health_screen(self, target_tab="daily"):
        self.clear_container()
        self.current_screen = "Health"

        header = tk.Frame(self.main_container, bg=THEME["secondary_b"], padx=20, pady=15)
        header.pack(fill=tk.X)

        pet_name = self.active_pet.name.upper() if self.active_pet else "PET"
        tk.Label(header, text=f"HEALTH HUB: {pet_name}", font=("Segoe UI", 14, "bold"), fg="white",
                 bg=THEME["secondary_b"]).pack(anchor="w")

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=THEME["bg"], borderwidth=0)
        style.configure('TNotebook.Tab', font=('Segoe UI', 9, 'bold'), padding=[10, 6], background="#E0E6E6",
                        foreground=THEME["text_gray"])
        style.map('TNotebook.Tab', background=[('selected', THEME["white"])],
                  foreground=[('selected', THEME["secondary_b"])])

        notebook = ttk.Notebook(self.main_container, style='TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tab_daily = tk.Frame(notebook, bg=THEME["white"], padx=15, pady=15)
        notebook.add(tab_daily, text=" 📝 Daily Tracking ")
        self.build_feature_list(tab_daily, [
            ("📝 Daily Log", "Log food quantities, mood, toilet habits", "daily_log"),
            ("🏃 Activity Tracker", "Monitor walks, training, active energy", "activity"),
            ("⚖️ Weight Tracker", f"Current: {self.active_pet.weight if self.active_pet else 0} kg — History", "weight")
        ])

        tab_care = tk.Frame(notebook, bg=THEME["white"], padx=15, pady=15)
        notebook.add(tab_care, text=" 🩺 Care & Meds ")
        self.build_feature_list(tab_care, [
            ("🥩 Feeding Tracker", "Set up meal schedules and portions", "feeding"),
            ("🩺 Symptom Checker", "Analyze anomalies and log health states", "symptom"),
            ("🛡️ Vaccines & Pills", "Anti-parasite treatments, routine shots", "vaccines")
        ])

        if target_tab == "care":
            notebook.select(tab_care)
        else:
            notebook.select(tab_daily)

    def build_feature_list(self, parent, items):
        if not self.active_pet:
            tk.Label(parent, text="Please add a pet first.", bg=THEME["white"], fg=THEME["text_gray"]).pack(pady=20)
            return

        for title, desc, feature_id in items:
            item_frame = tk.Frame(parent, bg=THEME["white"], highlightbackground="#F0F3F4", highlightthickness=1,
                                  cursor="hand2")
            item_frame.pack(fill=tk.X, pady=5, ipady=6)

            txt_frame = tk.Frame(item_frame, bg=THEME["white"], padx=8)
            txt_frame.pack(side=tk.LEFT, fill=tk.BOTH)

            tk.Label(txt_frame, text=title, font=("Segoe UI", 10, "bold"), fg=THEME["secondary_b"],
                     bg=THEME["white"]).pack(anchor="w")
            tk.Label(txt_frame, text=desc, font=("Segoe UI", 8), fg=THEME["text_gray"], bg=THEME["white"]).pack(
                anchor="w")

            tk.Label(item_frame, text="❯", font=("Segoe UI", 10), fg="#BDC3C7", bg=THEME["white"], padx=10).pack(
                side=tk.RIGHT)

            def make_cmd(fid=feature_id, t=title):
                if fid == "daily_log":
                    return lambda e: self.open_daily_log_module()
                return lambda e: self.open_history_viewer(fid, t)

            click_action = make_cmd()
            item_frame.bind("<Button-1>", click_action)
            for child in txt_frame.winfo_children():
                child.bind("<Button-1>", click_action)

    def open_history_viewer(self, feature_id, title):
        history_win = tk.Toplevel(self.root)
        history_win.geometry("340x500")
        history_win.title(f"{self.active_pet.name} - {title}")
        history_win.configure(bg=THEME["bg"])
        history_win.grab_set()

        header = tk.Frame(history_win, bg=THEME["secondary_b"], padx=15, pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text=title.upper(), font=("Segoe UI", 12, "bold"), fg="white", bg=THEME["secondary_b"]).pack(
            anchor="w")
        tk.Label(header, text=f"History log for {self.active_pet.name}", font=("Segoe UI", 8), fg="#BDC3C7",
                 bg=THEME["secondary_b"]).pack(anchor="w")

        canvas = tk.Canvas(history_win, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(history_win, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=THEME["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=320)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_win.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>",
                                                              lambda ev: canvas.yview_scroll(int(-1 * (ev.delta / 120)),
                                                                                             "units")))
        history_win.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        logs = []
        if hasattr(self.active_pet, "get_logs_by_type"):
            logs = self.active_pet.get_logs_by_type(feature_id)
        elif hasattr(self.active_pet, "health_logs") and feature_id in self.active_pet.health_logs:
            logs = self.active_pet.health_logs[feature_id]

        if not logs:
            empty_card = tk.Frame(scroll_frame, bg="white", padx=15, pady=20, highlightbackground="#EBF0F1",
                                  highlightthickness=1)
            empty_card.pack(fill=tk.X, pady=10)
            tk.Label(empty_card, text="📭 No records found yet.", font=("Segoe UI", 10, "bold"), fg=THEME["text_gray"],
                     bg="white").pack()
            tk.Label(empty_card, text="New entries will appear here after you log them.", font=("Segoe UI", 8),
                     fg=THEME["text_gray"], bg="white").pack(pady=(5, 0))
            return

        for log in reversed(logs):
            card = tk.Frame(scroll_frame, bg="white", padx=12, pady=10, highlightbackground="#EBF0F1",
                            highlightthickness=1)
            card.pack(fill=tk.X, pady=4)

            tk.Label(card, text=log.get("date", "Today"), font=("Segoe UI", 8, "bold"), fg=THEME["teal"],
                     bg="white").pack(anchor="w")

            tk.Label(card, text=log.get("value", ""), font=("Segoe UI", 10), fg=THEME["secondary_b"], bg="white",
                     wraplength=280, justify="left").pack(anchor="w", pady=(2, 4))

            if log.get("notes"):
                tk.Label(card, text=f"✍️ {log['notes']}", font=("Segoe UI", 8, "italic"), fg=THEME["text_gray"],
                         bg="white", wraplength=280, justify="left").pack(anchor="w")

    def show_more_screen(self):
        self.clear_container()
        self.current_screen = "More"

        header = tk.Frame(self.main_container, bg=THEME["secondary_b"], padx=20, pady=15)
        header.pack(fill=tk.X)
        tk.Label(header, text="APPLICATION SETTINGS", font=("Segoe UI", 14, "bold"), fg="white",
                 bg=THEME["secondary_b"]).pack(anchor="w")

        canvas = tk.Canvas(self.main_container, bg=THEME["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_container, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=THEME["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=340)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.root.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.root.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        user_card = tk.Frame(scroll_frame, bg="white", padx=15, pady=15, highlightbackground="#EBF0F1",
                             highlightthickness=1)
        user_card.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(user_card, text=self.user_profile["name"].upper(), font=("Segoe UI", 14, "bold"), fg="#111111",
                 bg="white").pack(anchor="w")
        tk.Label(user_card, text=self.user_profile["status"], font=("Segoe UI", 9), fg=THEME["text_gray"],
                 bg="white").pack(anchor="w", pady=(2, 8))

        btn_edit = tk.Button(user_card, text="⚙️ Edit Profile Data", bg=THEME["primary"], fg="white",
                             font=("Segoe UI", 8, "bold"),
                             relief=tk.FLAT, padx=10, pady=4, command=self.crud_update_profile)
        btn_edit.pack(anchor="w")

        tk.Label(scroll_frame, text="PREFERENCES", font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                 bg=THEME["bg"]).pack(anchor="w", padx=5, pady=(15, 4))

        notif_frame = tk.Frame(scroll_frame, bg="white", highlightbackground="#F2F4F4", highlightthickness=1)
        notif_frame.pack(fill=tk.X, pady=3, padx=5, ipady=6)
        tk.Label(notif_frame, text="🔔 Push Notifications", font=("Segoe UI", 10, "bold"), fg=THEME["secondary_b"],
                 bg="white").pack(side=tk.LEFT, padx=10)

        def toggle_notif():
            self.user_profile["notifications"] = "Disabled" if self.user_profile[
                                                                   "notifications"] == "Enabled" else "Enabled"
            self.show_more_screen()

        btn_toggle = tk.Button(notif_frame, text=self.user_profile["notifications"].upper(),
                               bg=THEME["teal"] if self.user_profile["notifications"] == "Enabled" else THEME[
                                   "text_gray"],
                               fg="white", font=("Segoe UI", 8, "bold"), relief=tk.FLAT, padx=8, command=toggle_notif)
        btn_toggle.pack(side=tk.RIGHT, padx=10)

        info_frame = tk.Frame(scroll_frame, bg="white", highlightbackground="#F2F4F4", highlightthickness=1)
        info_frame.pack(fill=tk.X, pady=3, padx=5, ipady=4)
        txt_f = tk.Frame(info_frame, bg="white", padx=10, pady=4)
        txt_f.pack(side=tk.LEFT)
        tk.Label(txt_f, text="📋 App Build Version", font=("Segoe UI", 10, "bold"), fg=THEME["secondary_b"],
                 bg="white").pack(anchor="w")
        tk.Label(txt_f, text="v2.4.0-pro (Stable Core)", font=("Segoe UI", 8), fg=THEME["text_gray"], bg="white").pack(
            anchor="w")

        tk.Label(scroll_frame, text="DANGER ZONE", font=("Segoe UI", 8, "bold"), fg="#E74C3C", bg=THEME["bg"]).pack(
            anchor="w", padx=5, pady=(20, 4))

        danger_card = tk.Frame(scroll_frame, bg="white", padx=15, pady=15, highlightbackground="#FADBD8",
                               highlightthickness=1)
        danger_card.pack(fill=tk.X, pady=5, padx=5)

        tk.Label(danger_card, text="Reset application cache and wipe workspace storage.", font=("Segoe UI", 8),
                 fg=THEME["text_gray"], bg="white").pack(anchor="w", pady=(0, 10))

        btn_wipe = tk.Button(danger_card, text="🗑️ WIPE ALL PETS DATA", bg="#E74C3C", fg="white",
                             font=("Segoe UI", 9, "bold"),
                             relief=tk.FLAT, pady=8, command=self.crud_delete_all_data)
        btn_wipe.pack(fill=tk.X)

    def crud_update_profile(self):
        win = tk.Toplevel(self.root)
        win.geometry("320x340")
        win.title("Edit Profile")
        win.configure(bg="white")
        win.grab_set()

        tk.Label(win, text="UPDATE USER DATA", bg=THEME["secondary_b"], fg="white", font=("Segoe UI", 11, "bold"),
                 pady=15).pack(fill=tk.X)

        form = tk.Frame(win, bg="white", padx=25, pady=15)
        form.pack(fill=tk.BOTH, expand=True)

        tk.Label(form, text="OWNER NAME", bg="white", fg=THEME["text_gray"], font=("Segoe UI", 8, "bold")).pack(
            anchor="w")
        e_name = tk.Entry(form, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 10))
        e_name.insert(0, self.user_profile["name"])
        e_name.pack(fill=tk.X, ipady=6, pady=(2, 12))

        tk.Label(form, text="BIO / OCCUPATION", bg="white", fg=THEME["text_gray"], font=("Segoe UI", 8, "bold")).pack(
            anchor="w")
        e_status = tk.Entry(form, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 10))
        e_status.insert(0, self.user_profile["status"])
        e_status.pack(fill=tk.X, ipady=6, pady=(2, 15))

        def save_profile():
            name_val = e_name.get().strip()
            status_val = e_status.get().strip()
            if not name_val:
                messagebox.showwarning("Validation Error", "Name cannot be empty!")
                return
            self.user_profile["name"] = name_val
            self.user_profile["status"] = status_val or "Pet Lover"
            win.destroy()
            self.show_more_screen()

        tk.Button(win, text="SAVE CHANGES", bg=THEME["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT, pady=10, command=save_profile).pack(fill=tk.X, padx=25, pady=(0, 20))

    def crud_delete_all_data(self):
        confirm = messagebox.askyesno(
            "Wipe Storage",
            "Are you absolutely sure you want to delete all pet profiles?\nThis action is permanent!"
        )
        if confirm:
            self.pets = []
            self.active_pet = None
            self.storage.save_pets([])
            messagebox.showinfo("Success", "Workspace storage cleared successfully 🗑️")
            self.show_more_screen()

    def open_my_pet_hub(self):
        my_pet_win = tk.Toplevel(self.root)
        app = MyPetHub(my_pet_win, self.storage, self.active_pet, self.pets, parent_menu=self)

        my_pet_win.protocol("WM_DELETE_WINDOW", app.close_and_sync)

    def render_navbar(self):
        nav_bar = tk.Frame(self.root, bg=THEME["white"], height=60, highlightbackground="#ECF0F1", highlightthickness=1)
        nav_bar.pack(fill=tk.X, side=tk.BOTTOM)

        nav_items = [
            ("🏠", "Home", self.show_home_screen),
            ("📊", "Health", self.show_health_screen),
            ("🐾", "My Pet", self.open_my_pet_hub),
            ("🤖", "AI", lambda: messagebox.showinfo("AI", "AI Vet Assistant coming soon! 🔥")),
            ("⚙️", "More", self.show_more_screen)
        ]

        for icon, name, command in nav_items:
            btn = tk.Frame(nav_bar, bg=THEME["white"], cursor="hand2")
            btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, pady=5)

            i_lab = tk.Label(btn, text=icon, font=("Segoe UI", 14), bg=THEME["white"])
            i_lab.pack()
            t_lab = tk.Label(btn, text=name, font=("Segoe UI", 7), bg=THEME["white"], fg=THEME["text_gray"])
            t_lab.pack()

            def make_lambda(cmd): return lambda e: cmd()

            click_action = make_lambda(command)

            btn.bind("<Button-1>", click_action)
            i_lab.bind("<Button-1>", click_action)
            t_lab.bind("<Button-1>", click_action)


class MyPetHub:
    def __init__(self, window, storage, active_pet, all_pets, parent_menu=None):
        self.window = window
        self.storage = storage
        self.active_pet = active_pet
        self.all_pets = all_pets
        self.parent_menu = parent_menu

        self.window.title("My Pet Workspace")
        self.window.geometry("360x700")
        self.window.configure(bg=THEME["bg"])
        self.window.grab_set()

        header = tk.Frame(self.window, bg=THEME["secondary_b"], padx=20, pady=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="MY PET SPACE", font=("Segoe UI", 14, "bold"), fg="white", bg=THEME["secondary_b"]).pack(
            side=tk.LEFT)

        tk.Button(header, text="✕", font=("Segoe UI", 12, "bold"), fg="white", bg=THEME["secondary_b"], relief=tk.FLAT,
                  cursor="hand2", command=self.close_and_sync).pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self.window, bg=THEME["bg"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=THEME["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=340)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def _on_hub_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.window.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_hub_mousewheel))
        self.window.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.render_hub()

    def close_and_sync(self):
        self.sync_with_parent()
        self.window.unbind_all("<MouseWheel>")
        self.window.destroy()

    def sync_with_parent(self):
        if self.parent_menu:
            self.parent_menu.refresh_current_screen()

    def render_hub(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.active_pet:
            empty_frame = tk.Frame(self.scrollable_frame, bg=THEME["bg"], pady=50)
            empty_frame.pack(fill=tk.X)
            tk.Label(empty_frame, text="No active pet profiles found.", bg=THEME["bg"], fg=THEME["text_gray"],
                     font=("Segoe UI", 10)).pack()
            tk.Button(empty_frame, text="➕ Create New Pet", bg=THEME["primary"], fg="white",
                      font=("Segoe UI", 10, "bold"),
                      relief=tk.FLAT, pady=10, command=self.add_new_pet_flow).pack(pady=15, fill=tk.X, padx=20)
            return

        pet = self.active_pet
        pet_icon = "🐕" if pet.__class__.__name__ == "Dog" else "🐈"

        nike_card = tk.Frame(self.scrollable_frame, bg="white", padx=20, pady=20, highlightbackground="#EBF0F1",
                             highlightthickness=1)
        nike_card.pack(fill=tk.X, pady=(10, 15), padx=5)

        top_row = tk.Frame(nike_card, bg="white")
        top_row.pack(fill=tk.X)

        tk.Label(top_row, text=pet.name.upper(), font=("Segoe UI", 20, "bold"), fg="#111111", bg="white").pack(
            side=tk.LEFT)
        tk.Label(top_row, text=pet_icon, font=("Segoe UI", 22), bg="white").pack(side=tk.RIGHT)

        sub_text = f"{pet.breed.upper()}  |  {pet.age} YEARS OLD"
        tk.Label(nike_card, text=sub_text, font=("Segoe UI", 9, "bold"), fg=THEME["text_gray"], bg="white").pack(
            anchor="w", pady=(4, 12))

        mgmt_bar = tk.Frame(nike_card, bg="white")
        mgmt_bar.pack(fill=tk.X, pady=(5, 0))

        tk.Button(mgmt_bar, text="✏️ Edit", bg=THEME["primary"], fg="white", font=("Segoe UI", 8, "bold"),
                  relief=tk.FLAT, padx=12, pady=3, command=self.edit_current_pet_flow).pack(side=tk.LEFT, padx=(0, 6))

        tk.Button(mgmt_bar, text="🗑️ Delete", bg="#E74C3C", fg="white", font=("Segoe UI", 8, "bold"),
                  relief=tk.FLAT, padx=12, pady=3, command=self.delete_current_pet).pack(side=tk.LEFT)

        tk.Label(self.scrollable_frame, text="PROFILE", font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                 bg=THEME["bg"]).pack(anchor="w", padx=5, pady=(10, 4))

        profile_items = [
            ("👤 Pet Profile", "View full data, bio and edit character attributes", "pet_profile"),
            ("🔲 QR Code ID", "Digital pet passport passport & contact tag share", "qr_code")
        ]
        self.build_section_list(profile_items)

        tk.Label(self.scrollable_frame, text="HEALTH RECORDS", font=("Segoe UI", 8, "bold"), fg=THEME["text_gray"],
                 bg=THEME["bg"]).pack(anchor="w", padx=5, pady=(15, 4))

        health_items = [
            ("⚖️ Vet Weight History", f"Last weight: {pet.weight} kg with datetime logs", "vet_weight"),
            ("💉 Vaccines & Serial Numbers", "Track batch numbers, shots & immunity duration", "vaccines_records"),
            ("🏥 Vet Visits & Checkups", "History of clinic entries and recommendations", "vet_visits"),
            ("💊 Prescribed Medications", "Active drugs course, descriptions & frequency", "medications")
        ]
        self.build_section_list(health_items)

        tk.Button(self.scrollable_frame, text="➕ ADD ANOTHER PET", bg="#ECF0F1", fg=THEME["secondary_b"],
                  font=("Segoe UI", 9, "bold"), relief=tk.FLAT, pady=10, command=self.add_new_pet_flow).pack(fill=tk.X,
                                                                                                             pady=(25,
                                                                                                                   10),
                                                                                                             padx=5)

    def build_section_list(self, items):
        for title, subtitle, section_id in items:
            row_frame = tk.Frame(self.scrollable_frame, bg="white", cursor="hand2", highlightbackground="#F2F4F4",
                                 highlightthickness=1)
            row_frame.pack(fill=tk.X, pady=3, padx=5, ipady=4)

            inner_text_frame = tk.Frame(row_frame, bg="white", padx=10, pady=6)
            inner_text_frame.pack(side=tk.LEFT, fill=tk.BOTH)

            tk.Label(inner_text_frame, text=title, font=("Segoe UI", 10, "bold"), fg=THEME["secondary_b"],
                     bg="white").pack(anchor="w")
            tk.Label(inner_text_frame, text=subtitle, font=("Segoe UI", 8), fg=THEME["text_gray"], bg="white").pack(
                anchor="w", pady=(1, 0))

            tk.Label(row_frame, text="❯", font=("Segoe UI", 10), fg="#CDD6D6", bg="white", padx=12).pack(side=tk.RIGHT)

            def make_click(sid=section_id, t=title):
                return lambda e: messagebox.showinfo(t, f"Opening Sub-module: '{sid}' for {self.active_pet.name} 🐕")

            action = make_click()
            row_frame.bind("<Button-1>", action)
            for child in inner_text_frame.winfo_children():
                child.bind("<Button-1>", action)

    @handle_error
    def add_new_pet_flow(self):
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
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(10, 0))
            e = tk.Entry(form, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 10))
            e.insert(0, placeholder)
            e.pack(fill=tk.X, ipady=8)
            entries[label] = e

        def submit():
            name = entries["Name"].get().strip()
            if not name:
                messagebox.showwarning("Error", "Name required")
                return

            cls = PET_CLASSES.get(pet_type_var.get())
            new_pet = cls(
                name=name,
                age=int(entries["Age"].get() or 1),
                weight=float(entries["Weight"].get() or 5.0),
                breed=entries["Breed"].get().strip() or "Unknown",
                temperament=entries["Character"].get().strip() or "Unknown"
            )

            self.all_pets.append(new_pet)
            self.storage.save_pets(self.all_pets)
            self.active_pet = new_pet

            self.sync_with_parent()
            self.render_hub()
            win.destroy()

        tk.Button(win, text="SAVE PET", bg=THEME["accent"], fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                  command=submit, pady=12).pack(fill=tk.X, padx=30, pady=20)

    def delete_current_pet(self):
        pet = self.active_pet
        if not pet:
            return

        confirm = messagebox.askyesno(
            "Delete Profile",
            f"Are you sure you want to delete {pet.name}?\nThis action cannot be undone."
        )
        if confirm:
            self.all_pets.remove(pet)
            self.storage.save_pets(self.all_pets)

            self.active_pet = self.all_pets[0] if self.all_pets else None

            messagebox.showinfo("Deleted", f"{pet.name}'s profile has been removed.")

            self.sync_with_parent()
            self.render_hub()

    def edit_current_pet_flow(self):
        pet = self.active_pet
        if not pet:
            return

        win = tk.Toplevel(self.window)
        win.geometry("340x500")
        win.configure(bg=THEME["white"])
        win.grab_set()
        win.focus_set()

        tk.Label(win, text=f"EDIT {pet.name.upper()}", bg=THEME["primary"], fg="white", font=("Segoe UI", 14, "bold"),
                 pady=20).pack(fill=tk.X)
        form = tk.Frame(win, bg=THEME["white"], padx=30, pady=20)
        form.pack(fill=tk.BOTH)

        fields = [
            ("Name", pet.name),
            ("Age", str(pet.age)),
            ("Weight", str(pet.weight)),
            ("Breed", pet.breed)
        ]
        entries = {}

        for label, current_val in fields:
            tk.Label(form, text=label.upper(), bg=THEME["white"], fg=THEME["text_gray"],
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(10, 0))
            e = tk.Entry(form, bg=THEME["bg"], relief=tk.FLAT, font=("Segoe UI", 10))
            e.insert(0, current_val)
            e.pack(fill=tk.X, ipady=8)
            entries[label] = e

        def save_changes():
            name_val = entries["Name"].get().strip()
            if not name_val:
                messagebox.showwarning("Warning", "Name field cannot be empty!")
                return

            try:
                pet.name = name_val
                pet.age = int(entries["Age"].get() or 0)
                pet.weight = float(entries["Weight"].get() or 0.0)
                pet.breed = entries["Breed"].get().strip() or "Unknown"

                self.storage.save_pets(self.all_pets)
                messagebox.showinfo("Success", "Pet profile updated successfully ✨")

                self.sync_with_parent()
                self.render_hub()
                win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for Age and Weight.")

        tk.Button(win, text="SAVE CHANGES", bg=THEME["accent"], fg="white", font=("Segoe UI", 10, "bold"),
                  relief=tk.FLAT,
                  command=save_changes, pady=12).pack(fill=tk.X, padx=30, pady=20)