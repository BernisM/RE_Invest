from bs4 import BeautifulSoup
import csv
import pandas as pd

# Charger le fichier HTML
html_file_path = "C:/Users/massw/OneDrive/Bureau/Programmation/RE_Invest/RE_Invest/26_rue_rhin_et_danube.txt"
save_name = "C:/Users/massw/OneDrive/Bureau/Programmation/RE_Invest/RE_Invest/26_rue_rhin_et_danube.csv"

# Charger le fichier HTML 
with open(html_file_path, 'r', encoding='utf-8') as file: 
    html_content = file.read() 

print(html_content)    

# Utiliser BeautifulSoup pour extraire les données 
soup = BeautifulSoup(html_content, 'html.parser') 
    
# Extraire les valeurs nécessaires 
addresses = [div.text.strip() for div in soup.find_all('div', class_='dvf-transaction__address')] 
features = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__feature')] 
area_values = [span['data-dvf-transaction-area'] for span in soup.find_all('span', class_='dvf-transaction__feature', 'data-dvf-transaction-area': True)] 
price_dates = [span.text.strip() for span in soup.find_all('span', class_='dvf-transaction__price-date')] 
price_values = [span['data-dvf-transaction-price-value'] for span in soup.find_all('span', class_='dvf-transaction__price-value', {'data-dvf-transaction-price-value': True})] 
    
# Créer un DataFrame pandas 
df = pd.DataFrame({ 'Address': addresses, 
                       'Feature': features, 
                       'Area Value': area_values, 
                       'Price Date': price_dates, 
                       'Price Value': price_values }) 
    
# Sauvegarder dans un fichier CSV 
df.to_csv(save_name, index=False)