from bs4 import BeautifulSoup
import csv, os, sys 
sys.path.append('C:/Users/massw/Anaconda3/Lib/site-packages')
import pandas as pd
from datetime import datetime
import numpy as np

today = datetime.today()

path = 'C:/Users/massw/OneDrive/Bureau/Programmation/RE_Invest/RE_Invest'

# Charger le fichier HTML
html_path = os.path.join(path,'4_rue_du_vert_buisson.html')
save_path = os.path.join(path,'4_rue_du_vert_buisson.csv')

# Charger le fichier HTML 
with open(html_path, 'r', encoding='utf-8') as file: 
    html_content = file.read()

# Utiliser BeautifulSoup pour extraire les données 
soup = BeautifulSoup(html_content, 'html.parser') 
    
# Extraire les valeurs nécessaires 
addresses = [div.text.strip() for div in soup.find_all('div', class_='dvf-transaction__address')] 
features = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__feature')] 
features_2 = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__feature')] 
area_values = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__feature', attrs={'data-dvf-transaction-area': True})]
price_dates = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__price-date')] 
price_values = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__price-value')]

# Récupérer dans la liste features_2 = nombre de pièce, 
# toutes les valeurs qui finissent pas 'pièces' ou le mot 'Studio'
def filter_by_pieces(value):
    return value.endswith('pièces') or value.endswith('Studio')
features_2 = list(filter(filter_by_pieces,features_2))

# Récupérer dans la liste features, le type de bien,
# maison ou appartement
def filter_by_type(value):
    return value.endswith('Appartement') or value.endswith('Maison')
features = list(filter(filter_by_type,features))

# Remove word 'pièces' in features_2 list
features_2 = [s.replace('pièces', '').replace(' ', '') for s in features_2]
# Remove word 'm2' in area_values list
area_values = [s.replace('m²', '').replace(' ', '') for s in area_values]
# Replace word 'Vendu(e) en'
price_dates = [s.replace('Vendu en', '').replace('Vendue en', '') for s in price_dates]
# Remove symbol '€' 
price_values = [s.replace('€', '').replace(' ', '') for s in price_values]
# Replace name appartement and maison by 1 et 0
ForH = [1 if f == 'Appartement' 
        else 0 if f == 'Maison' 
        else 2 if f == 'Immeuble' 
        else 3 for f in features]

# Dictionnaire pour convertir le mois francais en numeric
sales_dates = []
month_dict = {'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06',
              'juillet': '07', 'aout': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'}

# nombre de pièce, si studio nb pièce = 1
room = [1 if i == "Studio" else int(i) for i in features_2]

# Determine nomber of bedroom
chambres = [1 if r == 1 or r == 2 else int(r)-1 for r in room]

Sale_Since = []

for s_date in price_dates:
    month_str, year_str = s_date[:-4], s_date[-4:] # Extract month and year from the input string
    month_numeric = month_dict[month_str.strip()] # Convert the French month to numerical value
    date_object = datetime.strptime(month_numeric + year_str, '%m%Y') # Create a datetime object with the extracted values
    result_date = date_object.strftime('%m/%Y') # Format the datetime object as MM/YYYY
    sales_dates.append(result_date)
    diff = (today - date_object).days # Diff days
    Sale_Since.append(diff) # ADD values to Sale_Since list

print(Sale_Since)

# Vérifier que toutes les listes ont la même longueur
lengths = [len(addresses), len(features), len(room), len(area_values), len(price_dates), len(price_values)]
max_length = max(lengths)

# Print the lengths to debug
print("Lengths:", lengths)

# If lengths are not the same, pad the shorter lists with empty strings
addresses += [''] * (max_length - len(addresses))
features += [''] * (max_length - len(features))
room += [''] * (max_length - len(room))
area_values += [''] * (max_length - len(area_values))
price_dates += [''] * (max_length - len(price_dates))
price_values += [''] * (max_length - len(price_values))

# Print the lengths after padding
print("Lengths after padding:", [len(addresses), len(features), 
                                 len(room), len(area_values), 
                                 len(price_dates), len(price_values)])

# Calulate price per square meter 
price_m2 = [round(float(price) / float(area),2) for price, area in zip(price_values, area_values)]

# Créer un DataFrame pandas 
df = pd.DataFrame({ 'Address': addresses, 'Type' : features, 'Flat(1)_House(0)' : ForH,
                       'Room': room, 'Bedroom': chambres, 'Area (m2)': area_values, 
                       'Sale Date': sales_dates, 'Sale_Since': Sale_Since,
                       'Price (EUR)': price_values, 'Price/m2' : price_m2}) 

""" # Print lines where 'Room' is empty
empty_room_rows = df[df['Room'] == '']
print("Lines where 'Room' is empty:")
print(empty_room_rows) """

print(df.head(10))

# Si room est vide mettre la valeur équivalente au nombre de mètre carré
for index, row in df.iterrows():
    if pd.isna(row['Room']) or row['Room'] == '':
        area_value = float(row['Area (m²)'])

        # Find a row with equivalent 'Area (m²)' within +/- 10%
        matching_row = df[(df['Area (m²)'].astype(float) >= 0.9 * area_value) & (df['Area (m²)'].astype(float) <= 1.1 * area_value) & (df['Room'] != '')].head(1)

        # If a matching row is found, fill the 'Room' value
        if not matching_row.empty:
            df.at[index, 'Room'] = matching_row['Room'].values[0]

# Sauvegarder dans un fichier CSV 
df.to_csv(save_path, index=False)