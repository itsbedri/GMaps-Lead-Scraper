import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common import logger
import time


def extract_email(driver, link):
    if not link:
        return "N/A"
    
    driver.get(link)
    time.sleep(2)  # wait for page to load

    # we are going to look in each website individually for an email pattern
    try:
        page_source = driver.page_source
        email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_source)

        if not email_matches:
            return "N/A"
        
        unique_emails = list(set(email_matches))
        cleaned_emails = [e for e in unique_emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))]
        if cleaned_emails:
            logger.info(f"found emial: {cleaned_emails[0]}")
            return cleaned_emails[0]
        else:
            logger.info("No valid email found after cleaning.")
            return "N/A"
        
    except:
        logger.error("Error occurred while extracting email.")
        return "N/A"
 

def extract_info(driver, link):
    if not link:
        return "N/A", "N/A", "N/A"
    driver.get(link)
    
    wait = WebDriverWait(driver, 5)

    # Extract phone number
    try:
        phone_btn = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button[aria-label^='Phone:']")
            )
        )
        phone_num = phone_btn.get_attribute("aria-label").replace("Phone: ", "").strip()

    except:
        phone_num = "N/A"

    # Extract website
    try:
        website_btn = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[aria-label^='Website']")
            )
        )
        website = website_btn.get_attribute("href").strip()

    except:
        website = "N/A"

    # Extract email
    try:
        if website != "N/A":
            email = extract_email(driver, website)
        else:
            email = "N/A"
    except:
        email = "N/A"


    return phone_num, website, email