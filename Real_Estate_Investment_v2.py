import tkinter as tk
from tkinter import ttk
import sys 
sys.path.append('C:/Users/massw/Anaconda3/Lib/site-packages')
import tkcalendar
from datetime import datetime
import numpy as np
import locale
from Params_Invest import Parameter, Widgets

locale.setlocale(locale.LC_ALL, '')

today = datetime.today()

class InvestmentApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Investment Property Calculator")
        self.geometry("800x500")

        main_frame = tk.Frame(self)
        main_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
        
        parameters_frame = tk.Frame(main_frame)
        """ parameters_frame.place(relx=0.0, rely=0.0, relwidth=0.0, relheight=0) """
        
        widgets_frame = tk.Frame(main_frame)
        widgets_frame.place(relx=0.1, rely=0.2, relwidth=0.9, relheight=0.9)

        self.frame = {
            Parameter: Parameter(parameters_frame, self),
            Widgets: Widgets(widgets_frame, self)
        }

        for f in (Parameter, Widgets):
            frame = f(main_frame, self)
            self.frame[f] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        """ self.frame = {}
        for f in (Parameter, Widgets):
            frame = f(main_frame, self)
            self.frame[f] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
 """
        self.widget_states = {
            "price_entry": tk.BooleanVar(value=True), "contribution_entry": tk.BooleanVar(value=True),
            "negociation_entry": tk.BooleanVar(value=True), "negociation_price_entry": tk.BooleanVar(value=True),
            "years_combobox": tk.BooleanVar(value=True), "interest_rate_entry": tk.BooleanVar(value=True),
            "insurance_rate_entry": tk.BooleanVar(value=True), "sq_meter_entry": tk.BooleanVar(value=True),
            "renovation_entry": tk.BooleanVar(value=True),"renovation_price_entry": tk.BooleanVar(value=True)
        }

        # Placer les widgets
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=3)

        self.frame[Widgets].date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.frame[Widgets].price_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].price_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=1)
        
        self.frame[Widgets].contribution_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].contribution_entry.grid(row=1, column=3, padx=5, pady=5)
        
        self.frame[Widgets].negociation_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].negociation_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.frame[Widgets].negociation_price_label.grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].negociation_price_entry.grid(row=2, column=3, padx=5, pady=5)

        self.frame[Widgets].years_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].years_combobox.grid(row=3, column=1, padx=5, pady=5, columnspan=1)

        self.frame[Widgets].interest_rate_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].interest_rate_entry.grid(row=3, column=3, padx=5, pady=5)

        self.frame[Widgets].insurance_rate_label.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].insurance_rate_entry.grid(row=4, column=3, padx=5, pady=5)

        self.frame[Widgets].sq_meter_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].sq_meter_entry.grid(row=5, column=1, padx=5, pady=5)

        self.frame[Widgets].price_per_sq_meter_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].price_per_sq_meter_entry.grid(row=5, column=3, padx=5, pady=5)

        self.frame[Widgets].renovation_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].renovation_entry.grid(row=6, column=1, padx=5, pady=5)

        self.frame[Widgets].renovation_price_per_sq_m_label.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].renovation_price_per_sq_m_entry.grid(row=6, column=3, padx=5, pady=5)

        calculate_button = ttk.Button(self.frame[Widgets], text="Calculer", command=lambda: self.calculate())
        calculate_button.grid(row=7, column=0, columnspan=1, pady=20)
        self.bind('<Return>', lambda event: self.calculate())
        
        clear_button = ttk.Button(self.frame[Widgets], text="Effacer", command=lambda: self.frame[Parameter].effacer())
        clear_button.grid(row=7, column=1, columnspan=1, pady=20)

        cancel_button = ttk.Button(self.frame[Widgets], text="Fermer", command=self.cancel)
        cancel_button.grid(row=7, column=2, columnspan=1, pady=20)
        self.bind('<Escape>', self.cancel)

    def cancel(self, event=None):
        self.destroy()

    def show_results(self, results):
        if hasattr(self, 'result_window') and self.result_window.winfo_exists():
            self.result_window.destroy()
        
        result_window = tk.Toplevel(self)
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
        tree = ttk.Treeview(result_window, columns=columns, show="headings", height=5)

        # Définition du style pour surligner la ligne de l'annnée sélectionnée
        tree.tag_configure('selected_row', background='lightblue')

        # Centrer les données dans chaque colonne
        for col in columns:
            tree.column(col,anchor="center")

        # Ajouter les colonnes au tableau
        for col in columns:
            tree.heading(col, text=col)

        # Clear existing item in the Treeview
        for item in tree.get_children():
            tree.delete(item)

        for years in ["7", "10", "15", "20", "25"]:
            interest_rate = self.frame[Parameter].interest_rates[years]
            insurance_rate = self.frame[Parameter].insurance_rate_var.get()
            taeg = interest_rate + insurance_rate
            monthly_int_rate = taeg / 100 / 12
            loan = float(results['total_loan'])
            # Fonction PMT to calculate annual payment with interest
            mensualités = loan * monthly_int_rate / (1 - (1 + monthly_int_rate)**(-int(years) * 12))
            # Coût du crédit
            crd_cost = mensualités * int(years) * 12 - loan

            tree.insert("", "end", values=[years + " ans", f"{interest_rate:.2f}%", f"{taeg:.2f}%", f"{locale.format_string('%.2f', mensualités, grouping=True)}€", f"{locale.format_string('%.2f', crd_cost, grouping=True)}€"])

            # Obtenir la durée sélectionner
            selected_year = self.frame[Widgets].years_term_var.get() + " ans"

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
        date_value = self.frame[Parameter].date_var.get()
        purchase_price = float(self.frame[Widgets].price_entry.get())
        negociation_price = float(self.frame[Widgets].negociation_entry.get())
        last_price = purchase_price - negociation_price
        contribution_amount = float(self.frame[Widgets].contribution_entry.get())
        contribution_percentage = (contribution_amount / purchase_price) * 100
        years = int(self.frame[Widgets].years_combobox.get())
        interest_rate = float(self.frame[Widgets].interest_rate_entry.get())
        insurance_rate = float(self.frame[Widgets].insurance_rate_entry.get())
        sq_meter = float(self.frame[Widgets].sq_meter_entry.get())
        renovation_amount = float(self.frame[Widgets].renovation_entry.get())
        notary_fees = float(self.frame[Parameter].notary_fees_var.get())
        notary_fees = notary_fees * purchase_price

        total_loan = last_price + renovation_amount + notary_fees - contribution_amount
        
        results = {
            "total_loan": total_loan, "durée" : years,
            "taux": interest_rate + insurance_rate
        }

        # Affichez les résultats dans une nouvelle fenêtre
        self.show_results(results)

if __name__ == "__main__":
    app = InvestmentApp()
    app.mainloop()