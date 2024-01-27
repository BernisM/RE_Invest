import tkinter as tk
from tkinter import ttk
import tkcalendar
from datetime import datetime
import ast
import numpy as np
import locale

locale.setlocale(locale.LC_ALL, '')

today = datetime.today()

class InvestmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Property Calculator")

        a = 100000
        b = a * 0.1
        c = 55
        d = 500 * c

        # Variables
        self.date_var = tk.StringVar(value=today)    
        self.purchase_price_var = tk.DoubleVar(value=a)
        self.contribution_var = tk.DoubleVar(value=b)
        self.years_term_var = tk.StringVar(value=7)
        self.interest_rate_var = tk.DoubleVar(value=3.2)
        self.insurance_rate_var = tk.DoubleVar(value=0.17)
        self.sq_meter_var = tk.DoubleVar(value=c)
        self.price_per_sq_meter_var = tk.StringVar()
        self.renovation_var = tk.DoubleVar(value=d)
        self.renovation_price_per_sq_m_var = tk.StringVar()
        self.interest_rates = {"7": 3.2, "10": 3.4, "15": 3.85, "20": 4.05, "25": 4.2}
        self.notary_fees_var = tk.StringVar(value=0.08)

        # State variables for enabling/disabling widgets
        self.widget_states = {
            "price_entry": tk.BooleanVar(value=True),
            "contribution_entry": tk.BooleanVar(value=True),
            "years_combobox": tk.BooleanVar(value=True),
            "interest_rate_entry": tk.BooleanVar(value=True),
            "insurance_rate_entry": tk.BooleanVar(value=True),
            "sq_meter_entry": tk.BooleanVar(value=True),
            "renovation_entry": tk.BooleanVar(value=True),
            "renovation_price_entry": tk.BooleanVar(value=True)
        }

        # Widgets
        date_label = ttk.Label(root, text="Date d'achat:")
        date_entry = tkcalendar.Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day, datevar=self.date_var)
        date_entry.config(date_pattern='dd/MM/yyyy')

        price_label = ttk.Label(root, text="Prix d'achat (€):")
        price_entry = ttk.Entry(root, textvariable=self.purchase_price_var, validate="key", validatecommand=(root.register(self.val_calc), "%P"))
        price_entry.bind("<KeyRelease>", self.calculate_price_per_sq_meter)

        contribution_label = ttk.Label(root, text="Apport (€):")
        contribution_entry = ttk.Entry(root, textvariable=self.contribution_var, validate="key", validatecommand=(root.register(self.val_calc), "%P"))

        years_label = ttk.Label(root, text='Durée du prêt (années):')
        years_combobox = ttk.Combobox(root, textvariable=self.years_term_var, values=["7", "10", "15", "20", "25"], validate="key", validatecommand=(root.register(self.val_year), "%P"))
        years_combobox.bind("<<ComboboxSelected>>", self.update_interest_rate)

        interest_rate_label = ttk.Label(root, text="Taux d'intérêt (%):")
        interest_rate_entry = ttk.Entry(root, textvariable=self.interest_rate_var, state="readonly")

        insurance_rate_label = ttk.Label(root, text="Taux d'assurance (%):")
        insurance_rate_entry = ttk.Entry(root, textvariable=self.insurance_rate_var, state='readonly')

        sq_meter_label = ttk.Label(root, text="Nombre de mètre carré (m2):")
        sq_meter_entry = ttk.Entry(root, textvariable=self.sq_meter_var)
        sq_meter_entry.bind("<KeyRelease>", self.calculate_price_per_sq_meter)

        price_per_sq_meter_label = ttk.Label(root, text="Prix au mètre carré (€):")
        price_per_sq_meter_entry = ttk.Entry(root, textvariable=self.price_per_sq_meter_var, state="readonly")
        price_per_sq_meter_entry.bind("<KeyRelease>", self.calculate_price_per_sq_meter)

        renovation_label = ttk.Label(root, text="Montant rénovation (€):")
        renovation_entry = ttk.Entry(root, textvariable=self.renovation_var, validate="key", validatecommand=(root.register(self.val_calc), "%P"))
        renovation_entry.bind("<KeyRelease>", self.calculate_renovation_per_sq_meter)

        renovation_price_per_sq_m_label = ttk.Label(root, text="Coût au mètre carré (€):")
        renovation_price_per_sq_m_entry = ttk.Entry(root, textvariable=self.renovation_price_per_sq_m_var, state="readonly")

        # Placer les widgets
        root.columnconfigure(0,weight=1)
        root.columnconfigure(1,weight=3)

        date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        price_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        contribution_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        contribution_entry.grid(row=1, column=3, padx=5, pady=5)

        years_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        years_combobox.grid(row=2, column=1)

        interest_rate_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        interest_rate_entry.grid(row=2, column=3, padx=5, pady=5)

        insurance_rate_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        insurance_rate_entry.grid(row=3, column=3, padx=5, pady=5)

        sq_meter_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        sq_meter_entry.grid(row=4, column=1, padx=5, pady=5)

        price_per_sq_meter_label.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        price_per_sq_meter_entry.grid(row=4, column=3, padx=5, pady=5)

        renovation_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        renovation_entry.grid(row=5, column=1, padx=5, pady=5)

        renovation_price_per_sq_m_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        renovation_price_per_sq_m_entry.grid(row=5, column=3, padx=5, pady=5)

        # Bouton Calcul
        calculate_button = ttk.Button(root, text="Calculer", command=lambda: self.calculate())
        calculate_button.grid(row=10, column=0, columnspan=2, pady=20)
        root.bind('<Return>', lambda event: self.calculate())
        
        # Bouton Clear
        clear_button = ttk.Button(root, text="Effacer", command=self.effacer)
        clear_button.grid(row=10, column=1, columnspan=2, pady=20)

        # Bouton Cancel
        cancel_button = ttk.Button(root, text="Fermer", command=self.cancel)
        cancel_button.grid(row=10, column=2, columnspan=3, pady=20)
        root.bind('<Escape>', self.cancel)

    def val_calc(self, new_value):
        try:
            ast.parse(new_value, mode='eval')
            return True
        except SyntaxError:
            return False

    def calcul_amount(self, expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            print(f"Erreur de calcul : {e}")
            return None
    
    def val_year(self, new_value):
        return new_value == "" or new_value.replace(".","",1).isdigit()

    def update_interest_rate(self, event):
        selected_year = self.years_term_var.get()
        interest_rate = self.interest_rates.get(selected_year, 0)
        self.interest_rate_var.set(interest_rate)

    def effacer(self):
        self.date_var.set(today)
        self.purchase_price_var.set(0.0)
        self.contribution_var.set(0.0)
        self.years_term_var.set(7)
        self.interest_rate_var.set(3.2)
        self.insurance_rate_var.set(0.17)
        self.sq_meter_var.set(0.0)
        self.price_per_sq_meter_var.set("")
        self.renovation_var.set(0.0)
        self.renovation_price_per_sq_m_var.set("")

    def cancel(self, event=None):
        self.root.destroy()

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

    def show_results(self, results):
        if hasattr(self, 'result_window') and self.result_window.winfo_exists():
            self.result_window.destroy()
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Résultats")
        
        # Ajoutez des étiquettes + widgets 
        result_total = ttk.Label(result_window, text=f"Total du prêt: {locale.format_string('%.2f',results['total_loan'], grouping=True)}€")
        result_y = ttk.Label(result_window, text=f"Durée: {results['durée']} ans")
        result_rate = ttk.Label(result_window, text=f"Taux d'intérêt + Assurance: {results['taux']}%")
                         
        result_total.grid(row=0, column=0, padx=3, pady=3, sticky="w",columnspan=2)
        result_y.grid(row=1, column=0, padx=3, pady=3, sticky="w",columnspan=1)
        result_rate.grid(row=1, column=1, padx=3, pady=3, sticky="w")

        # Créer un tableau (Treeview) pour afficher les résultats
        columns = ["Durée annuel", "Taux d'intérêt", "Taux d'intérêt + Assurance", 'Mensualités', 'Coût du Crédit']
        tree = ttk.Treeview(result_window, columns=columns, show="headings")

        # Définition du style pour surligner la ligne de l'annnée sélectionnée
        tree.tag_configure('selected_row', background='lightblue')

        # Centrer les données dans chaque colonne
        for col in columns:
            tree.column(col,anchor="center")

        # Ajouter les colonnes au tableau
        for col in columns:
            tree.heading(col, text=col)

        for years in ["7", "10", "15", "20", "25"]:
            interest_rate = self.interest_rates[years]
            insurance_rate = self.insurance_rate_var.get()
            taeg = interest_rate + insurance_rate
            monthly_int_rate = taeg / 100 / 12
            loan = float(results['total_loan'])
            # Fonction PMT to calculate annual payment with interest
            mensualités = loan * monthly_int_rate / (1 - (1 + monthly_int_rate)**(-int(years) * 12))
            # Coût du crédit
            crd_cost = mensualités * int(years) * 12 - loan

            tree.insert("", "end", values=[years + " ans", f"{interest_rate:.2f}%", f"{taeg:.2f}%", f"{locale.format_string('%.2f', mensualités, grouping=True)}€", f"{locale.format_string('%.2f', crd_cost, grouping=True)}€"])

            # Obtenir la durée sélectionner
            selected_year = self.years_term_var.get() + " ans"

            # Trouver la ligne de l'année sélectionner dans le treeview
            for item in tree.get_children():
                if tree.item(item, "values")[0] == selected_year:
                    tree.item(item, tags=("selected_row",)) # Appliquer surligne bleu

        # Barre de défilement
        """ scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
        scrollbar.grid(row=2, column=1, sticky="nsew")
        tree.configure(yscrollcommand=scrollbar.set) """

        for col in columns:
            tree.column(col, stretch=tk.YES)

        tree.grid(row=3, column=0,padx=10, pady=10,sticky="w")


    def calculate(self, event=None):
        date_value = self.date_var.get()
        purchase_price = self.purchase_price_var.get()
        contribution_amount = self.contribution_var.get()
        contribution_percentage = (contribution_amount / purchase_price) * 100
        years = int(self.years_term_var.get())
        interest_rate = self.interest_rate_var.get()
        insurance_rate = self.insurance_rate_var.get()
        sq_meter = self.sq_meter_var.get()
        renovation_amount = self.renovation_var.get()
        notary_fees = float(self.notary_fees_var.get())
        notary_fees = notary_fees * purchase_price

        total_loan = purchase_price + renovation_amount + notary_fees - contribution_amount
        
        results = {
            "total_loan": total_loan, "durée" : years,
            "taux": interest_rate + insurance_rate
        }

        # Affichez les résultats dans une nouvelle fenêtre
        self.show_results(results)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentApp(root)
    root.mainloop()
