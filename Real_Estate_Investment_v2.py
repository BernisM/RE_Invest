import tkinter as tk
from tkinter import ttk
import sys, locale, csv, os
sys.path.append('C:/Users/massw/Anaconda3/Lib/site-packages')
import tkcalendar
from datetime import datetime
import numpy as np
from Params_Invest import Parameter, Widgets
import pandas as pd

locale.setlocale(locale.LC_ALL, '')

today = datetime.today()

class InvestmentApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.date_entry = tkcalendar.Calendar(self, selectmode='day')
        self.date_entry.config(date_pattern='dd/MM/yyyy')

        self.title("Investment Property Calculator")
        self.geometry("800x510")

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
            "years_combobox": tk.BooleanVar(value=True), "flat_house_combobox": tk.BooleanVar(value=True),
            "room_combobox": tk.BooleanVar(value=True),"interest_rate_entry": tk.BooleanVar(value=True),
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

        self.frame[Widgets].flat_house_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].flat_house_combobox.grid(row=5, column=1, padx=5, pady=5, columnspan=1)
        
        self.frame[Widgets].room_label.grid(row=5, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].room_combobox.grid(row=5, column=3, padx=5, pady=5, columnspan=1)

        self.frame[Widgets].sq_meter_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].sq_meter_entry.grid(row=6, column=1, padx=5, pady=5)

        self.frame[Widgets].price_per_sq_meter_label.grid(row=6, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].price_per_sq_meter_entry.grid(row=6, column=3, padx=5, pady=5)

        self.frame[Widgets].renovation_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.frame[Widgets].renovation_entry.grid(row=7, column=1, padx=5, pady=5)

        self.frame[Widgets].renovation_price_per_sq_m_label.grid(row=7, column=2, padx=5, pady=5, sticky="w")
        self.frame[Widgets].renovation_price_per_sq_m_entry.grid(row=7, column=3, padx=5, pady=5)

        calculate_button = ttk.Button(self.frame[Widgets], text="Calculer", command=lambda: self.calculate())
        calculate_button.grid(row=8, column=0, columnspan=1, pady=20)
        self.bind('<Return>', lambda event: self.calculate())
        
        clear_button = ttk.Button(self.frame[Widgets], text="Effacer", command=lambda: self.effacer())
        clear_button.grid(row=8, column=1, columnspan=1, pady=20)

        cancel_button = ttk.Button(self.frame[Widgets], text="Fermer", command=self.cancel)
        cancel_button.grid(row=8, column=2, columnspan=1, pady=20)
        self.bind('<Escape>', self.cancel)

    def cancel(self, event=None):
        self.destroy()

    def effacer(self):
        a = 70000
        b = a * 0.1
        c = 55
        d = 500 * c
        e = 20
        """ self.frame[Widgets].date_entry.tkcalendar.set_date(today.strftime('%d/%m/%Y'))  """#self.frame[Parameter].date_var
        self.frame[Widgets].price_entry.set(a)
        self.frame[Widgets].contribution_entry.set(int(a * 0.1))
        self.frame[Widgets].negociation_entry.set(e)
        self.frame[Widgets].negociation_price_entry.set(0)
        self.frame[Widgets].years_combobox.set(value="7")
        self.frame[Widgets].flat_house_combobox.set(value='Appartement')
        self.frame[Widgets].interest_rate_entry.set(value=3.20)
        self.frame[Widgets].insurance_rate_entry.set(value=0.17)
        self.frame[Widgets].sq_meter_entry.set(c)
        self.frame[Widgets].price_per_sq_meter_entry.set('')
        self.frame[Widgets].renovation_entry.set(d)
        self.frame[Widgets].renovation_price_per_sq_m_entry.set('')

    def show_results(self, results):
        if hasattr(self, 'result_window') and self.result_window.winfo_exists():
            self.result_window.destroy()
        
        result_window = tk.Toplevel(self)
        result_window.title("Résultats")

        # Create a frame to contain the result widgets
        result_frame = ttk.Frame(result_window)
        result_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Ajoutez des étiquettes + widgets 
        result_inital_price = ttk.Label(result_frame, text=f"Prix initial: {locale.format_string('%.2f',results['initial_price'], grouping=True)}€")
        result_final_price = ttk.Label(result_frame, text=f"Prix négocié: {locale.format_string('%.2f',results['last_price'], grouping=True)}€")
        result_notary = ttk.Label(result_frame, text=f"Frais de notaire: {locale.format_string('%.2f',results['notary_fees'], grouping=True)}€")
        result_contribution = ttk.Label(result_frame, text=f"Apport: {locale.format_string('%.2f',results['contribution_amount'], grouping=True)}€")
        result_renovation = ttk.Label(result_frame, text=f"Travaux: {locale.format_string('%.2f',results['renovation_price'], grouping=True)}€")

        result_total_nego = ttk.Label(result_frame, text=f"Total du prêt: {locale.format_string('%.2f',results['total_loan_nego'], grouping=True)}€", font=('Helvetica', '10', 'bold'))
        result_y = ttk.Label(result_frame, text=f"Durée: {results['durée']} ans", font=('Helvetica', '10', 'bold'))
        result_rate = ttk.Label(result_frame, text=f"Taux d'intérêt + Assurance: {results['taux']}%", font=('Helvetica', '10', 'bold'))
        result_credit_cost = ttk.Label(result_frame, text=f"Coût du crédit: {locale.format_string('%.2f',results['credit_cost'], grouping=True)}€", font=('Helvetica', '10', 'bold'))

        # ---------------------------------- 1ère LIGNE ------------------------------------------#
        result_inital_price.grid(row=0, column=0, padx=5, pady=5, sticky="w", columnspan=1)
        result_final_price.grid(row=0, column=2, padx=5, pady=5, sticky="w", columnspan=1)
        result_notary.grid(row=0, column=4, padx=5, pady=5, sticky="w", columnspan=1)
        result_contribution.grid(row=0, column=6, padx=5, pady=5, sticky="w", columnspan=1)
        result_renovation.grid(row=0, column=8, padx=5, pady=5, sticky="w", columnspan=1)

        # ------------------------------- SAUT DE LIGNE ------------------------------------------#
        result_total_nego.grid(row=1, column=0, padx=5, pady=5, sticky="w",columnspan=1)
        result_y.grid(row=1, column=2, padx=5, pady=5, sticky="w",columnspan=1)
        result_rate.grid(row=1, column=4, padx=5, pady=5, sticky="w", columnspan=1)
        result_credit_cost.grid(row=1, column=6, padx=5, pady=5, sticky="w", columnspan=1)

        # Create another frame for the Treeview
        tree_frame = ttk.Frame(result_window)
        tree_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Créer un tableau (Treeview) pour afficher les résultats
        columns = ["Durée annuel", "Taux d'intérêt", "Taux d'intérêt + Assurance", 'Mensualités', 'Coût du Crédit']
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=5)

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

        """ self.result_dict = {} """

        for years in ["7", "10", "15", "20", "25"]:
            interest_rate = self.frame[Parameter].interest_rates[years]
            insurance_rate = self.frame[Parameter].insurance_rate_var.get()
            taeg = interest_rate + insurance_rate
            monthly_int_rate = taeg / 100 / 12
            loan = float(results['total_loan_nego'])
            # Fonction PMT to calculate annual payment with interest
            mensualités = loan * monthly_int_rate / (1 - (1 + monthly_int_rate)**(-int(years) * 12))
            # Coût du crédit
            crd_cost = mensualités * int(years) * 12 - loan

            tree.insert("", "end", values=[years + " ans", f"{interest_rate:.2f}%", f"{taeg:.2f}%", f"{locale.format_string('%.2f', mensualités, grouping=True)}€", f"{locale.format_string('%.2f', crd_cost, grouping=True)}€"])

            # Obtenir la durée sélectionner
            selected_year = self.frame[Widgets].years_combobox.get() + " ans"
            """ selected_values = self.result_dict.get(selected_year, {}) """

            """ # Store values in the dictionary
            self.result_dict[years] = {"interest_rate": interest_rate,
                                            "taeg": taeg,
                                            "mensualités": mensualités,
                                            "crd_cost": crd_cost} """

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
        negociation_price = float(self.frame[Widgets].negociation_price_entry.get())
        last_price = purchase_price - negociation_price
        years = int(self.frame[Widgets].years_combobox.get())
        interest_rate = float(self.frame[Widgets].interest_rate_entry.get())
        insurance_rate = float(self.frame[Widgets].insurance_rate_entry.get())
        sq_meter = float(self.frame[Widgets].sq_meter_entry.get())
        renovation_amount = float(self.frame[Widgets].renovation_entry.get())
        notary_fees = float(self.frame[Parameter].notary_fees_var.get())
        notary_fees = notary_fees * purchase_price
        renovation_price = float(self.frame[Widgets].renovation_entry.get())
        ForH = self.frame[Parameter].flat_house_var.get()
        room = int(self.frame[Parameter].room_var.get())
        
        if float(self.frame[Widgets].contribution_entry.get()) >= last_price * 0.1:
            contribution_amount = float(self.frame[Widgets].contribution_entry.get())
        else:
            contribution_amount = last_price * 0.1

        total_loan_nego = last_price + renovation_amount + notary_fees - contribution_amount
        taeg = round(interest_rate + insurance_rate,2)
        monthly_int_rate = taeg / 100 / 12
        # Fonction PMT to calculate annual payment with interest
        mensualités = total_loan_nego * monthly_int_rate / (1 - (1 + monthly_int_rate)**(-int(years) * 12))
        # Coût du crédit
        crd_cost = round(mensualités * int(years) * 12 - total_loan_nego, 2)

        results = {
            "notary_fees": notary_fees, "durée" : years,
            "taux": taeg,
            "total_loan_nego": total_loan_nego, "initial_price": purchase_price,
            "contribution_amount": contribution_amount, "last_price": last_price, 
            "renovation_price": renovation_price, "credit_cost": crd_cost
        }

        # Définir le dictionnaire de mappage Flat_House_Building
        forh_mapping = {'Appartement': 1, 'Maison': 0, 'Immeuble': 2}
        ForH_val = forh_mapping.get(ForH, 3) # obtenir la valeur correspondante
        
        # obtenir la valeur correspondante chambre
        bedroom = 1 if room in [1, 2] else room - 1

        path = 'C:/Users/massw/OneDrive/Bureau/Programmation/RE_Invest/RE_Invest/My_notebooks'
        file = os.path.join(path,'To_Predict.csv')

        Sale_since = 0

        df_prediction = pd.DataFrame({
            "Flat(1)_House(0)" : ForH_val,
            "Room" : room, "bedroom" : bedroom,
            "Area (m2)" : sq_meter, "Sale_Since": Sale_since
        })

        df_prediction.to_csv(file, index=False)
        
        # Affichez les résultats dans une nouvelle fenêtre
        self.show_results(results)

if __name__ == "__main__":
    app = InvestmentApp()
    app.mainloop()