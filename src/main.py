import os
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
URL = "https://www.google.com/maps?hl=en"

from operation import scrape_all
from common import logger

st.set_page_config(page_title="Google Maps Scraper", page_icon=":mag:")
st.title("Google Maps Scraper :mag:")
st.markdown("Enter your search details below to start the bot.")
search_query = st.text_input("Search Query", placeholder="e.g. restaurants in New York")
filename = st.text_input("Filename", placeholder="e.g. results.csv")


def intialize_driver_func():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    return driver


if st.button("🚀 Start Scraping"):
    if not search_query:
        st.error("Please enter a search query!")
    else:
        driver = None
        try:
            with st.spinner("Bot is initializing... Check the Chrome window!"):
                driver = intialize_driver_func()
            with st.spinner("Bot is running... This may take a while!"):
                URL = "https://www.google.com/maps?hl=en" # Fixed URL
                driver.get(URL)
                wait = WebDriverWait(driver, 10)
                
                # Run your existing logic
                scrape_all(driver, search_query, wait, filename)
                
            st.success("✅ Scraping Complete!")
            
            # --- SHOW RESULTS ---
            if os.path.exists(filename):
                st.markdown("### 📊 Results Preview")
                # Read CSV to show it on screen
                df = pd.read_csv(filename)
                st.dataframe(df)
                
                # Provide download link
                with open(filename, "rb") as f:
                    st.download_button(
                        label="Download Results",
                        data=f,
                        file_name=filename,
                        mime="text/csv",
                    )
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            if driver:
                driver.quit()