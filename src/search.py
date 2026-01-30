#from ..common.logger import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_mech(driver, search_query, wait):
    searchBox = None

    try:
        search_box = wait.until(
            EC.presence_of_element_located((By.NAME, "q"))
         )

        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.Enter)
        
        
    except:
        pass
