import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from search import search_mech

URL = "https://www.google.com/maps?hl=en"
search_query = input("Enter your search query (e.g., 'Restaurants in Istanbul'): ")
filename = input("Enter the filename (e.g., 'leads.csv': ")


def intialize_driver_func():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def main():
    driver = intialize_driver_func()
    driver.get(URL)

    wait = WebDriverWait(driver, 10)
    

    search_mech(driver, search_query, wait)



if __name__ == "__main__":
    main()
