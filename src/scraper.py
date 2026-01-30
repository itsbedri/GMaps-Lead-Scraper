#from ..common.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_all(driver, search_query, wait):
    searchBox = None

    try:
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
         )

        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.Enter)


       scrollable_div_xpath = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[role='feed']")
            )
        )


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
                continue

            #logger.info(f"Extracting phone number from detail page for {name}...")

        enriched_data = []

        for index, row in enumerate(data):
            name = row[0]
            link = row[1]

            phone_num = extract_phone_num(driver, link)
            #logger.info(f"Found phone number: {phone_num} for {name}")

            enriched_data.append([name, link, phone_num])


        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Link", "Phone Number"])
            writer.writerows(enriched_data)

        #logger.info(f"Data saved to {filename}")

        input("Press Enter to close the browser...")
    except Exception as e:
        #logger.error(f"An error occurred: {e}")
        input("Error encountered. Press Enter to close the browser...")

    finally:
        driver.quit()




    except:
        pass
