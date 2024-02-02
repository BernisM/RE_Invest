from bs4 import BeautifulSoup
import csv, os, sys 
sys.path.append('C:/Users/massw/Anaconda3/Lib/site-packages')
import pandas as pd
from datetime import datetime
import numpy as np

path = 'C:/Users/massw/OneDrive/Bureau/Programmation/RE_Invest/RE_Invest'

# Charger le fichier HTML
html_path = os.path.join(path,'26_rue_rhin_et_danube.html')
save_path = os.path.join(path,'26_rue_rhin_et_danube.csv')

# Charger le fichier HTML 
with open(html_path, 'r', encoding='utf-8') as file: 
    html_content = file.read()

# Utiliser BeautifulSoup pour extraire les données 
soup = BeautifulSoup(html_content, 'html.parser') 
    
# Extraire les valeurs nécessaires 
addresses = [div.text.strip() for div in soup.find_all('div', class_='dvf-transaction__address')] 
features = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__feature')] 
area_values = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__feature', attrs={'data-dvf-transaction-area': True})]
price_dates = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__price-date')] 
price_values = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__price-value')]

def filter_by_pieces(value):
    return value.endswith('pièces') or value.endswith('Studio')
features = list(filter(filter_by_pieces,features))

features = [s.replace('pièces', '').replace(' ', '') for s in features]
area_values = [s.replace('m²', '').replace(' ', '') for s in area_values]
price_dates = [s.replace('Vendu en', '') for s in price_dates]
price_values = [s.replace('€', '').replace(' ', '') for s in price_values]

sales_dates = []
month_dict = {'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04', 'mai': '05', 'juin': '06',
              'juillet': '07', 'août': '08', 'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'}

room = [1 if i == "Studio" else i for i in features]


for s_date in price_dates:
# Extract month and year from the input string
    month_str, year_str = s_date[:-4], s_date[-4:]
# Convert the French month to numerical value
    month_numeric = month_dict.get(month_str.lower(), '01')
# Create a datetime object with the extracted values
    date_object = datetime.strptime(month_numeric + year_str, '%m%Y')
# Format the datetime object as MM/YYYY
    result_date = date_object.strftime('%m/%Y')
    sales_dates.append(result_date)

# Vérifier que toutes les listes ont la même longueur
lengths = [len(addresses), len(room), len(area_values), len(price_dates), len(price_values)]
max_length = max(lengths)

# Print the lengths to debug
print("Lengths:", lengths)

# If lengths are not the same, pad the shorter lists with empty strings
addresses += [''] * (max_length - len(addresses))
room += [''] * (max_length - len(room))
area_values += [''] * (max_length - len(area_values))
price_dates += [''] * (max_length - len(price_dates))
price_values += [''] * (max_length - len(price_values))

# Print the lengths after padding
print("Lengths after padding:", [len(addresses), len(room), len(area_values), len(price_dates), len(price_values)])

# Créer un DataFrame pandas 
df = pd.DataFrame({ 'Address': addresses, 
                       'Room': room, 
                       'Area (m²)': area_values, 
                       'Sale Date': sales_dates, 
                       'Price (€)': price_values }) 

# Print lines where 'Room' is empty
empty_room_rows = df[df['Room'] == '']
print("Lines where 'Room' is empty:")
print(empty_room_rows)

# Si room est vide mettre la valeur équivlente au nombre de mètre carré
for index, row in df.iterrows():
    if pd.isna(row['Room']) or row['Room'] == '':
        area_value = float(row['Area (m²)'])

        # Find a row with equivalent 'Area (m²)' within +/- 10%
        matching_row = df[(df['Area (m²)'].astype(float) >= 0.9 * area_value) & (df['Area (m²)'].astype(float) <= 1.1 * area_value) & (df['Room'] != '')].head(1)

        # If a matching row is found, fill the 'Room' value
        if not matching_row.empty:
            df.at[index, 'Room'] = matching_row['Room'].values[0]

print(df.tail(4))

# Sauvegarder dans un fichier CSV 
df.to_csv(save_path, index=False)