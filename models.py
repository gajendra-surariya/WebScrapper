from pydantic import BaseModel, Field
from typing import Optional

class ScrapeSettings(BaseModel):
    page_limit: Optional[int] = Field(
        default=0,
        description="Limit the number of pages to scrape (0 means scrape until no more products found)."
    )
    proxy: Optional[str] = Field(
        default=None,
        description="Proxy string (e.g. 'http://proxy:port') to use for scraping."
    )

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
