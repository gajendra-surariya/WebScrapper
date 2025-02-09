## Requirements

- **Python:** 3.7 or higher
- **Dependencies:**
  - FastAPI
  - uvicorn
  - requests
  - beautifulsoup4
  - pydantic

## Overview

This project is a FastAPI-based web scraper designed to extract product information (name, price, and image) from the url. It supports optional settings such as limiting the number of pages to scrape and using a proxy for requests. The project uses an object-oriented approach with abstractions for storage and notifications, making it easy to extend or swap out components in the future.

## Features

- **Scraping:** Extracts product details (title, price, image) from each page.
- **Optional Settings:**  
  - `page_limit`: Limit the number of pages to scrape.
  - `proxy`: Provide a proxy string for HTTP requests.
- **Storage:** Stores scraped data in a local JSON file (`products.json`). Designed for easy integration with other storage strategies.
- **Notification:** Notifies the scraping status (total products scraped and updated) via the console.
- **Caching:** Prevents updating products whose price hasn't changed.
- **Retry Mechanism:** Implements a simple retry logic when a page fails to load.
- **Authentication:** Secures the endpoint using a static token.
