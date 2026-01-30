import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.logger import logger

filename = input("Enter the filename (e.g., 'leads.csv': ")
query = input("Enter your search query (e.g., 'Restaurants in Istanbul'): ")


def extract_phone_num(driver, url):
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 5)
        # Look for the phone button (aria-label starts with 'Phone:')
        phone_btn = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[aria-label^='Phone:']")
            )
        )
        return phone_btn.get_attribute("aria-label").replace("Phone: ", "").strip()
    except:
        return "N/A"


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )

    url = "https://www.google.com/maps?hl=en"
    logger.info(f"Navigating to {url}")
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    search_box = None

    try:
        logger.info("Waiting for the search box to be present...")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

        search_query = query
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)

        logger.info("Waiting for search results to load...")

        time.sleep(5)  # wait for results to load

        logger.info("scrolling down the results...")
        scrollable_div_xpath = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
        )

        logger.info("Scrolling down...")
        for i in range(10):  # scroll 10 times
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div_xpath,
            )
            time.sleep(2)  # wait for new results to load

        logger.info("Extracting data...")
        cards = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        data = []

        for card in cards:
            try:
                link_tag = card.find_element(By.TAG_NAME, "a")
                name = link_tag.get_attribute("aria-label")
                link = link_tag.get_attribute("href")

                if name and link:
                    data.append([name, link])
                    print(f"Extracted: {name}")
            except Exception as e:
                print(f"Error extracting data from a card: {e}")
                continue

            logger.info(f"Extracting phone number from detail page for {name}...")

        enriched_data = []

        for index, row in enumerate(data):
            name = row[0]
            link = row[1]

            phone_num = extract_phone_num(driver, link)
            logger.info(f"Found phone number: {phone_num} for {name}")

            enriched_data.append([name, link, phone_num])

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Link", "Phone Number"])
            writer.writerows(enriched_data)

        logger.info(f"Data saved to {filename}")

        input("Press Enter to close the browser...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        input("Error encountered. Press Enter to close the browser...")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
