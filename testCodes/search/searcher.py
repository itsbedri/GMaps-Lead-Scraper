from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# chrome configuration
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US")
driver = webdriver.Chrome(options=options)


url = "https://www.google.com/maps?hl=en"

# start a new browser session
print("Opening Google Maps...")
driver.get(url)

# professional wait implementation
wait = WebDriverWait(driver, 15)

try:
    print("Waiting for the cookie acceptance button...")

    xpath_generic = "//form//button[last()]"

    accept_cookies_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath_generic))
    )
    accept_cookies_button.click()
    print("Cookie acceptance button clicked.")
    time.sleep(2)  # wait for 2 seconds to ensure the dialog is closed
except:
    print("No cookie acceptance button found.")

    search_box = None

try:
    print("Locating the search box...")

    try:
        search_box = wait.until(
        EC.presence_of_element_located((By.ID, "searchboxinput"))
    )
    except:
        pass

    if not search_box:

        try:
            print("By ID not found, trying NAME...")
            # use the global name for search box
            search_box = driver.find_element(By.NAME, "q")
        except:
            pass

    if not search_box:
        print("By ID and NAME not found, trying TAG_NAME...")
        try:
            search_box = driver.find_element(By.TAG_NAME, "input")
            print("✅ Found by Input Tag!")
        except:
            pass


    if search_box:
        print("Search box located.")
        search_query = "Eiffel Tower"
        print(f"Entering search query: {search_query}")
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)
        print("Search query submitted.")
    else:
        print("❌ Search box not found. by ID, NAME, or TAG_NAME.")
        print("Search box not found.")
        raise Exception("Search box not found.")



    print("Waiting for search results to load...")
    time.sleep(5)  # wait for results to load
    input("Press Enter to close the browser...")
    driver.quit()

except Exception as e:
    print(f"An error occurred: {e}")
    input("Error encountered. Press Enter to close the browser...")
    driver.quit()
