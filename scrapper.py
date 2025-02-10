
import os
import re
import time
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from models import Product
from config import RETRY_COUNT, RETRY_DELAY

class Scraper:
    def __init__(self, page_limit: int = 0, proxy: Optional[str] = None):
        self.page_limit = page_limit
        self.proxy = {"http": proxy, "https": proxy} if proxy else None

    def fetch_page(self, url: str) -> Optional[str]:
        attempt = 0
        while attempt < RETRY_COUNT:
            try:
                response = requests.get(url, proxies=self.proxy, timeout=10)
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"Error fetching {url}: Status code {response.status_code}. Retrying...")
            except Exception as e:
                print(f"Exception fetching {url}: {e}. Retrying...")
            attempt += 1
            time.sleep(RETRY_DELAY)
        return None

    def parse_products(self, html: str) -> List[Product]:
        soup = BeautifulSoup(html, "html.parser")
        product_elements = soup.select("ul.products li.product")   # elements of Product
        products: List[Product] = []
        for element in product_elements:
            title_elem = element.select_one("h2.woo-loop-product__title")  # element of title 
            price_elem = element.select_one("span.price")  # element of price
            image_elem = element.select_one("img")   # image element
            if title_elem and price_elem and image_elem:
                title = title_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True)
                price = self.extract_price(price_text)
                image_url = image_elem.get("src")
                image_path = self.download_image(image_url, title)
                products.append(Product(
                    product_title=title,
                    product_price=price,
                    path_to_image=image_path
                ))
        return products

    def extract_price(self, price_text: str) -> float:
        clean_text = re.sub(r'[^\d\.]', '', price_text)
        try:
            return float(clean_text)
        except ValueError:
            return 0.0

    def download_image(self, url: str, title: str) -> str:
        image_folder = "images"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        safe_title = re.sub(r'\W+', '_', title)
        extension = url.split(".")[-1].split("?")[0]
        file_name = f"{safe_title}.{extension}"
        file_path = os.path.join(image_folder, file_name)
        try:
            r = requests.get(url, proxies=self.proxy, stream=True, timeout=10)
            if r.status_code == 200:
                with open(file_path, "wb") as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
        return file_path

    def scrape(self) -> List[Product]:
        products: List[Product] = []
        page = 2
        while True:
            if self.page_limit and page > self.page_limit:
                break

            url = f"https://dentalstall.com/shop/page/{page}/"
            print(f"Scraping {url}")
            html = self.fetch_page(url)
            if not html:
                print(f"Failed to retrieve page {page}. Ending scraping.")
                break

            page_products = self.parse_products(html)
            if not page_products:
                print("No products found on this page. Ending scraping.")
                break

            products.extend(page_products)
            page += 1

        return products
