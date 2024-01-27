import tkinter as tk
from tkinter import ttk
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
        self.geometry("800x600")

        main_frame = tk.Frame(self)
        main_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)
        
        parameters_frame = tk.Frame(main_frame)
        parameters_frame.place(relx=0.1, rely=0.1, relwidth=0.5, relheight=1)
        
        widgets_frame = tk.Frame(main_frame)
        widgets_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

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
            "price_entry": tk.BooleanVar(value=True),
            "contribution_entry": tk.BooleanVar(value=True),
            "years_combobox": tk.BooleanVar(value=True),
            "interest_rate_entry": tk.BooleanVar(value=True),
            "insurance_rate_entry": tk.BooleanVar(value=True),
            "sq_meter_entry": tk.BooleanVar(value=True),
            "renovation_entry": tk.BooleanVar(value=True),
            "renovation_price_entry": tk.BooleanVar(value=True)
        }

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        date_label = ttk.Label(self, text="Date d'achat:")
        date_entry = tkcalendar.Calendar(self, selectmode='day', year=today.year, month=today.month, day=today.day, datevar=self.frame[Parameter].date_var)
        date_entry.config(date_pattern='dd/MM/yyyy')

        price_label = ttk.Label(self, text="Prix d'achat (€):")
        price_entry = ttk.Entry(self, textvariable=self.frame[Parameter].purchase_price_var, validate="key", validatecommand=(self.register(self.frame[Parameter].val_calc), "%P"))
        price_entry.bind("<KeyRelease>", self.frame[Parameter].calculate_price_per_sq_meter)

        contribution_label = ttk.Label(self, text="Apport (€):")
        contribution_entry = ttk.Entry(self, textvariable=self.frame[Parameter].contribution_var, validate="key", validatecommand=(self.register(self.frame[Parameter].val_calc), "%P"))

        years_label = ttk.Label(self, text='Durée du prêt (années):')
        years_combobox = ttk.Combobox(self, textvariable=self.frame[Parameter].years_term_var, values=["7", "10", "15", "20", "25"], validate="key", validatecommand=(self.register(self.frame[Parameter].val_year), "%P"))
        years_combobox.bind("<<ComboboxSelected>>", self.frame[Parameter].update_interest_rate)

        interest_rate_label = ttk.Label(self, text="Taux d'intérêt (%):")
        interest_rate_entry = ttk.Entry(self, textvariable=self.frame[Parameter].interest_rate_var, state="readonly")

        insurance_rate_label = ttk.Label(self, text="Taux d'assurance (%):")
        insurance_rate_entry = ttk.Entry(self, textvariable=self.frame[Parameter].insurance_rate_var, state='readonly')

        sq_meter_label = ttk.Label(self, text="Nombre de mètre carré (m2):")
        sq_meter_entry = ttk.Entry(self, textvariable=self.frame[Parameter].sq_meter_var)
        sq_meter_entry.bind("<KeyRelease>", self.frame[Parameter].calculate_price_per_sq_meter)

        price_per_sq_meter_label = ttk.Label(self, text="Prix au mètre carré (€):")
        price_per_sq_meter_entry = ttk.Entry(self, textvariable=self.frame[Parameter].price_per_sq_meter_var, state="readonly")
        price_per_sq_meter_entry.bind("<KeyRelease>", self.frame[Parameter].calculate_price_per_sq_meter)

        renovation_label = ttk.Label(self, text="Montant rénovation (€):")
        renovation_entry = ttk.Entry(self, textvariable=self.frame[Parameter].renovation_var, validate="key", validatecommand=(self.register(self.frame[Parameter].val_calc), "%P"))
        renovation_entry.bind("<KeyRelease>", self.frame[Parameter].calculate_renovation_per_sq_meter)

        renovation_price_per_sq_m_label = ttk.Label(self, text="Coût au mètre carré (€):")
        renovation_price_per_sq_m_entry = ttk.Entry(self, textvariable=self.frame[Parameter].renovation_price_per_sq_m_var, state="readonly")

        # widgets in the grid

        calculate_button = ttk.Button(self, text="Calculer", command=lambda: self.calculate())
        calculate_button.grid(row=10, column=0, columnspan=2, pady=20)
        self.bind('<Return>', lambda event: self.frame[Parameter].calculate())
        
        clear_button = ttk.Button(self, text="Effacer", command=self.frame[Parameter].effacer)
        clear_button.grid(row=10, column=1, columnspan=2, pady=20)

        cancel_button = ttk.Button(self, text="Fermer", command=self.cancel)
        cancel_button.grid(row=10, column=2, columnspan=3, pady=20)
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
            selected_year = self.frame[Parameter].years_term_var.get() + " ans"

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
        purchase_price = self.frame[Parameter].purchase_price_var.get()
        contribution_amount = self.frame[Parameter].contribution_var.get()
        contribution_percentage = (contribution_amount / purchase_price) * 100
        years = int(self.frame[Parameter].years_term_var.get())
        interest_rate = self.frame[Parameter].interest_rate_var.get()
        insurance_rate = self.frame[Parameter].insurance_rate_var.get()
        sq_meter = self.frame[Parameter].sq_meter_var.get()
        renovation_amount = self.frame[Parameter].renovation_var.get()
        notary_fees = float(self.frame[Parameter].notary_fees_var.get())
        notary_fees = notary_fees * purchase_price

        total_loan = purchase_price + renovation_amount + notary_fees - contribution_amount
        
        results = {
            "total_loan": total_loan, "durée" : years,
            "taux": interest_rate + insurance_rate
        }

        # Affichez les résultats dans une nouvelle fenêtre
        self.show_results(results)

if __name__ == "__main__":
    app = InvestmentApp()
    app.mainloop()
