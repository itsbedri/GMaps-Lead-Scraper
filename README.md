# GMaps-Lead-Scraper


⚠️ Disclaimer
This project is for educational only. Please respect Google's robots.txt policy and Terms of Service. Do not use this tool for large-scale commercial scraping without permission.

# Google Maps Lead Extractor

> **A robust, full-stack scraping bot engineered to harvest business intelligence from Google Maps at scale.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 📖 Overview
This tool automates the process of generating B2B leads from Google Maps. Unlike basic scrapers that crash on dynamic content, this bot utilizes a **two-phase architecture** to safely extract business names, links, and **hidden phone numbers** without triggering StaleElementReferenceExceptions.

It solves the "Infinite Scroll" problem by programmatically manipulating the DOM to load hundreds of results before extraction begins.

![Demo Result]
you can check it in leads.csv file, to get a grasp of how the info is stored

##  Key Features
- ** Infinite Scrolling Engine:** Automatically detects the scrollable feed and forces Google Maps to load 50-100+ results (bypassing the initial 20-item limit).
- ** Stale Element Protection:** Uses a "Harvest & Enrich" pattern. It collects stable permalinks first, then visits them individually, preventing the common "element lost" crash.
- ** Data Enrichment:** Navigates to individual business profiles to extract verified phone numbers hidden behind `aria-label` tags.
- ** Cookie Wall Bypass:** Automatically detects and accepts Google's consent dialogs (supports both English and international variants).
- **Smart Waits:** Replaces brittle `time.sleep` with Selenium's `WebDriverWait` and `ExpectedConditions` for network-independent stability.

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Core Library:** Selenium WebDriver (Chrome)
- **Dependency Management:** `webdriver-manager` (Auto-updates Chromium drivers)
- **Data Handling:** `csv` module (Native, lightweight export)

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/itsbedri/GMaps-Lead-Scraper.git](https://github.com/itsbedri/GMaps-Lead-Scraper.git)
   cd GMaps-Lead-Scraper


