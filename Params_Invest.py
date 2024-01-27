import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime
import locale
import ast

locale.setlocale(locale.LC_ALL, '')

today = datetime.today()

a = 70000
b = a * 0.1
c = 55
d = 500 * c
e = 20

class Parameter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.date_var = tk.StringVar(value=today)
        self.contribution_var = tk.DoubleVar(value=b)
        self.negociation_var = tk.StringVar(value=e)
        self.negociation_price_var = tk.StringVar(0)
        self.purchase_price_var = tk.DoubleVar(value=a)
        self.years_term_var = tk.StringVar(value=7)
        self.interest_rate_var = tk.DoubleVar(value=3.2)
        self.insurance_rate_var = tk.DoubleVar(value=0.17)
        self.sq_meter_var = tk.DoubleVar(value=c)
        self.price_per_sq_meter_var = tk.StringVar()
        self.renovation_var = tk.DoubleVar(value=d)
        self.renovation_price_per_sq_m_var = tk.StringVar()
        self.interest_rates = {"7": 3.2, "10": 3.4, "15": 3.85, "20": 4.05, "25": 4.2}
        self.notary_fees_var = tk.StringVar(value=0.08)

    def calculate_contribution(self):
        return self.purchase_price_var.get() * 0.1
    
    def effacer(self):
        self.date_var.set(today)
        self.purchase_price_var.set(0.0)
        self.contribution_var.set(0.0)
        self.negociation_var.set(0)
        self.negociation_price_var.set(0)
        self.years_term_var.set(7)
        self.interest_rate_var.set(3.2)
        self.insurance_rate_var.set(0.17)
        self.sq_meter_var.set(0.0)
        self.price_per_sq_meter_var.set("")
        self.renovation_var.set(0.0)
        self.renovation_price_per_sq_m_var.set("")
    
    def val_year(self, new_value):
        return new_value == "" or new_value.replace(".","",1).isdigit()
    
    def val_calc(self, new_value):
        try:
            ast.parse(new_value, mode='eval')
            return True
        except SyntaxError:
            return False
        
    def update_interest_rate(self, event):
        selected_year = self.years_term_var.get()
        interest_rate = self.interest_rates.get(selected_year, 0)
        self.interest_rate_var.set(interest_rate)
    
    def calculate_price_per_sq_meter(self, event=None):
        try:
            purchase_price = self.purchase_price_var.get()
            sq_meter = self.sq_meter_var.get()

            if purchase_price > 0 and sq_meter > 0:
                price_per_sq_meter = purchase_price / sq_meter
                self.price_per_sq_meter_var.set(f"{price_per_sq_meter:.2f}")
            else:
                self.price_per_sq_meter_var.set("N/A")

        except (ZeroDivisionError, ValueError):
            self.price_per_sq_meter_var.set("N/A")

    def calculate_renovation_per_sq_meter(self, event=None):
        try:
            renovation_price = self.renovation_var.get()
            sq_meter_1 = self.sq_meter_var.get()

            if renovation_price >= 0 and sq_meter_1 > 0:
                renovation_per_sq_meter = renovation_price / sq_meter_1
                self.renovation_price_per_sq_m_var.set(f"{renovation_per_sq_meter:.2f}")
            else:
                self.renovation_price_per_sq_m_var.set("N/A")

        except (ZeroDivisionError, ValueError):
            self.renovation_price_per_sq_m_var.set("N/A")

    def val_price(self, event):
        return self.purchase_price_var.get() * self.negociation_var.get()

class Widgets(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parameter = Parameter(parent, controller)

        date_label = ttk.Label(self, text="Date d'achat:")
        date_entry = tkcalendar.Calendar(self, selectmode='day', year=today.year, month=today.month, day=today.day, datevar=self.parameter.date_var)
        date_entry.config(date_pattern='dd/MM/yyyy')

        self.price_label = ttk.Label(self, text="Prix d'achat (€):")
        self.price_entry = ttk.Entry(self, textvariable=self.parameter.purchase_price_var, validate="key", validatecommand=(self.parameter.val_calc, "%P"))
        self.price_entry.bind("<KeyRelease>", self.parameter.calculate_price_per_sq_meter)

        contribution_label = ttk.Label(self, text="Apport (€):")
        contribution_entry = ttk.Entry(self, textvariable=self.parameter.contribution_var, validate="key", validatecommand=(self.parameter.val_calc, "%P"))

        years_label = ttk.Label(self, text='Durée du prêt (années):')
        years_combobox = ttk.Combobox(self, textvariable=self.parameter.years_term_var, values=["7", "10", "15", "20", "25"], validate="key", validatecommand=(self.parameter.val_year, "%P"))
        years_combobox.bind("<<ComboboxSelected>>", self.parameter.update_interest_rate)

        interest_rate_label = ttk.Label(self, text="Taux d'intérêt (%):")
        interest_rate_entry = ttk.Entry(self, textvariable=self.parameter.interest_rate_var, state="readonly")

        insurance_rate_label = ttk.Label(self, text="Taux d'assurance (%):")
        insurance_rate_entry = ttk.Entry(self, textvariable=self.parameter.insurance_rate_var, state='readonly')

        sq_meter_label = ttk.Label(self, text="Nombre de mètre carré (m2):")
        sq_meter_entry = ttk.Entry(self, textvariable=self.parameter.sq_meter_var)
        sq_meter_entry.bind("<KeyRelease>", self.parameter.calculate_price_per_sq_meter)

        price_per_sq_meter_label = ttk.Label(self, text="Prix au mètre carré (€):")
        price_per_sq_meter_entry = ttk.Entry(self, textvariable=self.parameter.price_per_sq_meter_var, state="readonly")
        price_per_sq_meter_entry.bind("<KeyRelease>", self.parameter.calculate_price_per_sq_meter)

        renovation_label = ttk.Label(self, text="Montant rénovation (€):")
        renovation_entry = ttk.Entry(self, textvariable=self.parameter.renovation_var, validate="key", validatecommand=(self.parameter.val_calc, "%P"))
        renovation_entry.bind("<KeyRelease>", self.parameter.calculate_renovation_per_sq_meter)

        renovation_price_per_sq_m_label = ttk.Label(self, text="Coût au mètre carré (€):")
        renovation_price_per_sq_m_entry = ttk.Entry(self, textvariable=self.parameter.renovation_price_per_sq_m_var, state="readonly")
