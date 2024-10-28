# src/ui.py
import tkinter as tk
from tkinter import messagebox, Canvas, Frame
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from src.menu import get_menu
from src.order import Order
from src.transaction import TransactionHistory

class CashRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caisse Enregistreuse - Restaurant")
        self.root.geometry("900x700")  # Taille initiale
        self.order = Order()
        self.menu_items = get_menu()
        self.transaction_history = TransactionHistory()

        # Palette de couleurs chaleureuses
        self.bg_color = "#faf3e0"
        self.menu_bg = "#8c7b75"
        self.btn_color = "#b5651d"

        self.root.configure(bg=self.bg_color)

        # Activer la responsivité de la grille principale
        self.root.columnconfigure(0, weight=2)  # Agrandir l'espace du menu
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=2)

        # Initialiser l'interface utilisateur
        self.create_ui()

        # Gestionnaire de redimensionnement avec délai pour éviter les appels fréquents
        self.resize_id = None
        self.root.bind("<Configure>", self.on_resize)

    def create_ui(self):
        self.create_menu_display()
        self.create_order_display()
        self.create_total_display()
        self.create_history_section()

    def create_menu_display(self):
        self.menu_frame = Frame(self.root, bg=self.menu_bg)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10, rowspan=2)

        self.menu_frame.columnconfigure(0, weight=1)
        self.menu_frame.rowconfigure(0, weight=1)

        self.menu_canvas = Canvas(self.menu_frame, bg=self.menu_bg, highlightthickness=0)
        self.menu_canvas.grid(row=0, column=0, sticky="nsew")

        scroll_y = ttk.Scrollbar(self.menu_frame, orient="vertical", command=self.menu_canvas.yview)
        scroll_y.grid(row=0, column=1, sticky="ns")

        self.menu_canvas.configure(yscrollcommand=scroll_y.set)
        self.menu_canvas.bind('<Configure>', lambda e: self.menu_canvas.configure(scrollregion=self.menu_canvas.bbox("all")))

        self.scrollable_frame = Frame(self.menu_canvas, bg=self.menu_bg)
        self.menu_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        tk.Label(self.scrollable_frame, text="Menu", font=("Arial", 14, "bold"), bg=self.menu_bg, fg="white").grid(row=0, column=0, columnspan=3, pady=5)

        # Charger les images originales une seule fois et les mettre en cache
        self.original_images = []
        for item in self.menu_items:
            pil_img = Image.open(item.image)
            self.original_images.append(pil_img)

        # Création dynamique des boutons de menu en grille
        self.menu_buttons = []
        self.menu_images = []
        self.image_size = 100  # Taille fixe pour les images
        columns = 3  # Nombre de colonnes dans la grille

        for idx, item in enumerate(self.menu_items):
            # Redimensionner l'image mise en cache
            pil_img = self.original_images[idx]
            pil_img_resized = ImageOps.fit(pil_img, (self.image_size, self.image_size), Image.LANCZOS)
            img = ImageTk.PhotoImage(pil_img_resized)
            self.menu_images.append(img)  # Garder une référence de l'image

            btn = tk.Button(self.scrollable_frame, image=img, text=f"{item.name}\n{item.price:.2f} MAD",
                            compound=tk.TOP, font=("Arial", 9),
                            bg=self.btn_color, fg="white", borderwidth=0,
                            command=lambda i=item: self.add_to_order(i),
                            width=self.image_size, height=self.image_size + 40)  # +40 pour le texte
            row = (idx // columns) + 1  # +1 pour tenir compte du label "Menu"
            col = idx % columns
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.menu_buttons.append(btn)

        # Configurer les colonnes pour qu'elles aient le même poids
        for i in range(columns):
            self.scrollable_frame.columnconfigure(i, weight=1, uniform='col')

        # Configurer les lignes pour qu'elles aient le même poids
        total_rows = (len(self.menu_items) + columns - 1) // columns + 1  # +1 pour la ligne du label
        for i in range(1, total_rows):
            self.scrollable_frame.rowconfigure(i, weight=1, uniform='row')

    def create_order_display(self):
        self.order_frame = Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        self.order_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(self.order_frame, text="Commande", font=("Arial", 14, "bold"), bg=self.bg_color, fg="#333").pack(anchor="w", padx=5, pady=5)

        self.order_list = tk.Listbox(self.order_frame, font=("Arial", 11))
        self.order_list.pack(fill="both", expand=True, padx=5, pady=5)

    def create_total_display(self):
        self.total_frame = Frame(self.root, bg="#333", padx=10, pady=10)
        self.total_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        self.total_label = tk.Label(self.total_frame, text="Total: 0.00 MAD", font=("Arial", 13, "bold"), fg="white", bg="#333")
        self.total_label.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(self.total_frame, text="Effacer Commande", font=("Arial", 9, "bold"),
                                 bg="#d9534f", fg="white", command=self.clear_order, borderwidth=0)
        clear_button.pack(side=tk.RIGHT, padx=10)

        confirm_button = tk.Button(self.total_frame, text="Confirmer Commande", font=("Arial", 9, "bold"),
                                   bg="#5cb85c", fg="white", command=self.confirm_order, borderwidth=0)
        confirm_button.pack(side=tk.RIGHT, padx=10)

    def create_history_section(self):
        history_frame = Frame(self.root, bg=self.bg_color, padx=10, pady=10)
        history_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        tk.Label(history_frame, text="Historique des Transactions", font=("Arial", 14, "bold"), bg=self.bg_color, fg="#333").pack(anchor="w", padx=5, pady=5)

        columns = ("Date", "Articles", "Total")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("Articles", text="Articles")
        self.history_tree.heading("Total", text="Total (MAD)")
        self.history_tree.column("Date", width=150)
        self.history_tree.column("Articles", width=500)
        self.history_tree.column("Total", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        self.update_history_tree()

    def add_to_order(self, item):
        self.order.add_item(item)
        self.order_list.insert(tk.END, f"{item.name} - {item.price:.2f} MAD")
        self.update_total()

    def clear_order(self):
        self.order.reset_order()
        self.order_list.delete(0, tk.END)
        self.update_total()

    def confirm_order(self):
        total = self.order.calculate_total()
        self.transaction_history.add_transaction(self.order.items, total)
        messagebox.showinfo("Confirmation", f"Commande confirmée ! Total: {total:.2f} MAD")
        self.clear_order()
        self.update_history_tree()

    def update_total(self):
        total = self.order.calculate_total()
        self.total_label.config(text=f"Total: {total:.2f} MAD")

    def update_history_tree(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)

        transactions = self.transaction_history.get_transactions()
        for transaction in transactions:
            timestamp = transaction["timestamp"]
            items = ", ".join([f"{name} ({price:.2f} MAD)" for name, price in transaction["items"]])
            total = transaction["total"]
            self.history_tree.insert("", "end", values=(timestamp, items, f"{total:.2f} MAD"))

    def on_resize(self, event):
        # Utiliser un délai pour éviter les appels fréquents lors du redimensionnement
        if self.resize_id:
            self.root.after_cancel(self.resize_id)
        self.resize_id = self.root.after(200, self.do_resize)

    def do_resize(self):
        # Redimensionner les images et les boutons en fonction de la taille de la fenêtre
        width = self.menu_frame.winfo_width()
        columns = 3  # Nombre de colonnes dans la grille
        padding = 20  # Somme des padx
        available_width = width - (columns + 1) * padding
        new_size = max(80, available_width // columns)

        for idx, btn in enumerate(self.menu_buttons):
            # Redimensionner l'image mise en cache
            pil_img = self.original_images[idx]
            pil_img_resized = ImageOps.fit(pil_img, (new_size, new_size), Image.LANCZOS)
            img = ImageTk.PhotoImage(pil_img_resized)
            self.menu_images[idx] = img  # Mettre à jour la référence de l'image
            btn.config(image=img, width=new_size, height=new_size + 40)  # +40 pour le texte
            btn.image = img  # Garder une référence pour éviter le garbage collection

            # Ajuster la taille de la police du texte sur le bouton
            font_size = max(9, new_size // 10)
            btn.config(font=("Arial", font_size))

        # Ajuster la hauteur minimale des lignes dans la grille pour s'adapter aux nouveaux boutons
        total_rows = (len(self.menu_items) + columns - 1) // columns + 1  # +1 pour le label "Menu"
        for i in range(1, total_rows):
            self.scrollable_frame.rowconfigure(i, minsize=new_size + 60)  # +60 pour le texte et les marges

        # Réinitialiser l'ID de redimensionnement
        self.resize_id = None
