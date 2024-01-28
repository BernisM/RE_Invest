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
        self.contribution_var = tk.DoubleVar(value=int(b))
        self.negociation_var = tk.StringVar(value=e)
        self.negociation_price_var = tk.DoubleVar(0)
        self.purchase_price_var = tk.DoubleVar(value=a)
        self.years_term_var = tk.StringVar(value=7)
        self.interest_rate_var = tk.DoubleVar(value=3.20)
        self.insurance_rate_var = tk.DoubleVar(value=0.17)
        self.sq_meter_var = tk.DoubleVar(value=c)
        self.price_per_sq_meter_var = tk.StringVar()
        self.renovation_var = tk.DoubleVar(value=d)
        self.renovation_price_per_sq_m_var = tk.StringVar()
        self.interest_rates = {"7": 3.20, "10": 3.40, "15": 3.85, "20": 4.05, "25": 4.20}
        self.notary_fees_var = tk.StringVar(value=0.08)

    """def calculate_contribution(self):
        purchase_price = self.purchase_price_var.get()
        cal_contrib = purchase_price * 0.10
        self.contribution_var.set(f"{cal_contrib:.2f}".rstrip('0').rstrip('.'))"""
    
    def effacer(self):
        self.date_var.set(today)
        self.purchase_price_var.set(a)
        self.contribution_var.set(int(a * 0.1))
        self.negociation_var.set(e)
        self.negociation_price_var.set(0)
        self.years_term_var.set("7")
        self.update_interest_rate(None)  # Call the method to update interest rate
        self.insurance_rate_var.set(0.17)
        self.sq_meter_var.set(c)
        self.calculate_price_per_sq_meter(None)  # Call the method to calculate price per sq meter
        self.renovation_var.set(d)
        self.calculate_renovation_per_sq_meter(None)
    
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

    def val_price(self, event=None):
        try:
            purchase_price = self.purchase_price_var.get()
            negociation_percent = float(self.negociation_var.get())

            negociation_price = int(purchase_price * (negociation_percent / 100))
            self.negociation_price_var.set(f"{negociation_price:.2f}".rstrip('0').rstrip('.'))

        except (ZeroDivisionError, ValueError):
            pass
    
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

class Widgets(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parameter = Parameter(parent, controller)

        self.date_label = ttk.Label(self, text="Date d'achat:")
        self.date_entry = tkcalendar.Calendar(self, selectmode='day', year=today.year, month=today.month, day=today.day, datevar=self.parameter.date_var)
        self.date_entry.config(date_pattern='dd/MM/yyyy')

        self.price_label = ttk.Label(self, text="Prix d'achat (€):")
        self.price_entry = ttk.Entry(self, textvariable=self.parameter.purchase_price_var, validate="key", validatecommand=(self.parameter.val_calc, "%P"))
        self.price_entry.bind("<KeyRelease>", self.parameter.calculate_price_per_sq_meter)

        self.contribution_label = ttk.Label(self, text="Apport (€):")
        self.contribution_entry = ttk.Entry(self, textvariable=self.parameter.contribution_var, validate="key", validatecommand=(self.parameter.val_calc, "%P"))
#        self.contribution_entry.bind("<KeyRelease>", self.parameter.calculate_contribution)

        self.negociation_label = ttk.Label(self, text="Négociation (%):")
        self.negociation_entry = ttk.Entry(self, textvariable=self.parameter.negociation_var, validate="key", validatecommand=(self.register(self.parameter.val_price), "%P"))
        self.negociation_entry.bind("<KeyRelease>", self.parameter.val_price)

        self.negociation_price_label = ttk.Label(self, text="Négociation (€):")
        self.negociation_price_entry = ttk.Entry(self, textvariable=self.parameter.negociation_price_var, state="readonly")

        self.years_label = ttk.Label(self, text='Durée du prêt (années):')
        self.years_combobox = ttk.Combobox(self, textvariable=self.parameter.years_term_var, values=["7", "10", "15", "20", "25"], validate="key", validatecommand=(self.parameter.val_year, "%P"))
        self.years_combobox.bind("<<ComboboxSelected>>", self.parameter.update_interest_rate)

        self.interest_rate_label = ttk.Label(self, text="Taux d'intérêt (%):")
        self.interest_rate_entry = ttk.Entry(self, textvariable=self.parameter.interest_rate_var, state="readonly")

        self.insurance_rate_label = ttk.Label(self, text="Taux d'assurance (%):")
        self.insurance_rate_entry = ttk.Entry(self, textvariable=self.parameter.insurance_rate_var, state='readonly')

        self.sq_meter_label = ttk.Label(self, text="Nombre de mètre carré (m2):")
        self.sq_meter_entry = ttk.Entry(self, textvariable=self.parameter.sq_meter_var)
        self.sq_meter_entry.bind("<KeyRelease>", self.parameter.calculate_price_per_sq_meter)

        self.price_per_sq_meter_label = ttk.Label(self, text="Prix au mètre carré (€):")
        self.price_per_sq_meter_entry = ttk.Entry(self, textvariable=self.parameter.price_per_sq_meter_var, state="readonly")
        self.price_per_sq_meter_entry.bind("<KeyRelease>", self.parameter.calculate_price_per_sq_meter)

        self.renovation_label = ttk.Label(self, text="Montant rénovation (€):")
        self.renovation_entry = ttk.Entry(self, textvariable=self.parameter.renovation_var, validate="key", validatecommand=(self.parameter.val_calc, "%P"))
        self.renovation_entry.bind("<KeyRelease>", self.parameter.calculate_renovation_per_sq_meter)

        self.renovation_price_per_sq_m_label = ttk.Label(self, text="Coût au mètre carré (€):")
        self.renovation_price_per_sq_m_entry = ttk.Entry(self, textvariable=self.parameter.renovation_price_per_sq_m_var, state="readonly")
