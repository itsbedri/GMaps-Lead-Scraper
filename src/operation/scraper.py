from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

from common import logger
from operation.extract import extract_info

def scrape_all(driver, search_query, wait, filename) -> None:
    search_box = None

    try:
        logger.info(f"Searching for '{search_query}'...")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

        logger.info("Entering search query...")
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)


        logger.info("Waiting for search results to load...")
        
        scrollable_div_xpath = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
        )

        logger.info("Scrolling through the results to load all entries...")
        for i in range(10):  # scroll 10 times
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div_xpath,
            )

        time.sleep(2)

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
                logger.error(f"Error extracting data from a card: {e}")
        
           

        enriched_data = []

        logger.info("Extracting phone numbers from detail pages...")
        for index, row in enumerate(data):
            name = row[0]
            link = row[1]

            phone_num, website, email = extract_info(driver, link)
            logger.info(f"Found phone number: {phone_num}, website: {website}, and email: {email} for {name}")

            enriched_data.append([name, link, phone_num, website, email])

        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Link", "Phone Number", "Website", "Email"])
            writer.writerows(enriched_data)

        logger.info(f"Data saved to {filename}")

        input("Press Enter to close the browser...")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        input("Error encountered. Press Enter to close the browser...")

    finally:
        driver.quit()
