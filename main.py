# main.py
import tkinter as tk
from src.ui import CashRegisterApp

if __name__ == "__main__":
    root = tk.Tk()
    app = CashRegisterApp(root)
    root.mainloop()
