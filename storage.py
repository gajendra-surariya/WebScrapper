import os
import json
from typing import List, Dict
from models import Product

class Storage:
    def save(self, products: List[Product]) -> None:
        raise NotImplementedError

    def load(self) -> Dict[str, Product]:
        raise NotImplementedError

class JSONStorage(Storage):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Dict[str, Product]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    return {item["product_title"]: Product(**item) for item in data}
            except Exception as e:
                print(f"Error loading JSON DB: {e}")
        return {}

    def save(self, products: List[Product]) -> None:
        data = [product.dict() for product in products]
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
