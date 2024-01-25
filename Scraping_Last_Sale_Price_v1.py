from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = "https:/www.meilleursagents.com/prix-immobilier/dvf/grenoble-38000/avenue-rhin-et-danube-1131337117/26/"
""" chromedriver_path = "C:\\Users\massw\Downloads\chromedriver_win32.zip\chromedriver" """

def scrape_apartments():
    base_url = url

    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()

    try:
        driver.get(base_url)

        # Wait for loading page
        driver.implicitly_wait(10)  

        # Get data
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')

        # Get info with classes
        addresses = [address.text.strip() for address in soup.find_all(class_='dvf-transaction__address')]
        features = [feature.text.strip() for feature in soup.find_all(class_='dvf-transaction__feature')]
        prices = [price.text.strip() for price in soup.find_all(class_='dvf-transaction__price-value')]

        # Display result
        for address, feature, price in zip(addresses, features, prices):
            print(f"Adresse: {address}, Caractéristique: {feature}, Prix: {price}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_apartments()


