from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US")
driver = webdriver.Chrome(options=options)

url = "https://www.google.com/maps?hl=en"
print("Opening Google Maps...")
driver.get(url)

wait = WebDriverWait(driver, 10)
search_box = None
try:
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
except:
    pass

if search_box:
    try:
        print("Search box located.")
        search_query = "Coffee shops in Istanbul"
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)

        print("Waiting for search results to load...")
        time.sleep(5)  # wait for results to load

        print("Starting to scroll down the results...")
        scrollable_div_xpath = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='feed']"))
        )

        print("Scrolling down...")

        for i in range(10):  # scroll 10 times
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight",
                scrollable_div_xpath,
            )
            print(f"Scrolled {i + 1} times")
            time.sleep(2)  # wait for new results to load

            print("\n\n\n\n")
            item = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
            print(f"Number of items loaded: {len(item)}")
            count = len(item)

            if count >= 50:
                print("Loaded 50 items, stopping scroll.")
                break
            elif count == 0:
                print("No items found, stopping scroll.")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

driver.quit()
