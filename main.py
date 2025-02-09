
from fastapi import FastAPI, Depends
from models import ScrapeSettings
from scraper import Scraper
from storage import JSONStorage
from notifier import ConsoleNotifier
from dependencies import verify_token
from config import JSON_DB_PATH

app = FastAPI()

@app.post("/scrape", dependencies=[Depends(verify_token)])
def scrape_endpoint(settings: ScrapeSettings):

    
    storage = JSONStorage(JSON_DB_PATH)
    notifier = ConsoleNotifier()

    
    existing_products = storage.load()
    cache = {title: prod for title, prod in existing_products.items()}

    
    scraper = Scraper(page_limit=settings.page_limit, proxy=settings.proxy)
    scraped_products = scraper.scrape()

    scraped_count = len(scraped_products)
    updated_count = 0

    
    for product in scraped_products:
        if product.product_title in cache:
            if cache[product.product_title].product_price == product.product_price:
                continue  
        cache[product.product_title] = product
        updated_count += 1

    
    storage.save(list(cache.values()))
    notifier.notify(scraped_count, updated_count)

    return {"scraped": scraped_count, "updated": updated_count}
