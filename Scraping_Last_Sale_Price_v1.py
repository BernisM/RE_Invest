import csv, os, sys, time
sys.path.append('/Users/marvinbernis/opt/anaconda3/lib/python3.9/site-packages')

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https:/www.meilleursagents.com/prix-immobilier/dvf/grenoble-38000/avenue-rhin-et-danube-1131337117/26/"
""" chromedriver_path = "C:\\Users\massw\Downloads\chromedriver_win32.zip\chromedriver" """

def scrape_apartments():
    base_url = url

    # Set up the Selenium WebDriver with headless mode
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(base_url)
        
        # Wait for the page to load (adjust the duration as needed)
        time.sleep(10)

        # Wait for the elements to be visible
        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'dvf-transaction__address')))
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'dvf-transaction__feature')))
        wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'dvf-transaction__price-value')))

        # Get text from elements
        addresses = [address.text.strip() for address in driver.find_elements(By.CLASS_NAME, 'dvf-transaction__address')]
        features = [feature.text.strip() for feature in driver.find_elements(By.CLASS_NAME, 'dvf-transaction__feature')]
        prices = [price.text.strip() for price in driver.find_elements(By.CLASS_NAME, 'dvf-transaction__price-value')]

        # Display extracted data
        print("Addresses:", addresses)
        print("Features:", features)
        print("Prices:", prices)

        # Create a list of dictionaries
        data = [{'Adresse': address, 'Caractéristique': feature, 'Prix': price} for address, feature, price in zip(addresses, features, prices)]

        # Display data
        print("Data:", data)

        # Save data to CSV
        csv_file_path = '/Users/marvinbernis/Desktop/Investissement locatif/RE_Invest/RE_Invest/scraped_data.csv'
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Adresse', 'Caractéristique', 'Prix']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            writer.writerows(data)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_apartments()