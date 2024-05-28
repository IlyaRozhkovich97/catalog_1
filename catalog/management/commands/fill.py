import os
from django.core.management import BaseCommand
import json
from config.settings import FIXTURES_ROOT
from catalog.models import Category, Product


class Command(BaseCommand):
    filename = "products.json"
    file_path = os.path.join(FIXTURES_ROOT, filename)

    @staticmethod
    def json_read(file_path, model_type):
        """Чтение данных из фикстуры"""
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [item for item in data if item["model"].split(".")[1] == model_type]

    def handle(self, *args, **options):
        products_data = Command.json_read(Command.file_path, "product")
        categories_data = Command.json_read(Command.file_path, "category")

        Product.objects.all().delete()
        Category.objects.all().delete()

        categories_to_create = [
            Category(
                pk=category["pk"],
                name=category["fields"]["name"],
                description=category["fields"]["description"]
            )
            for category in categories_data
        ]
        Category.objects.bulk_create(categories_to_create)

        products_to_create = [
            Product(
                name=product["fields"]["name"],
                description=product["fields"]["description"],
                image=product["fields"]["image"],
                category_id=product['fields']['category'],
                purchase_price=product["fields"]["purchase_price"],
                created_at=product["fields"]["created_at"],
                updated_at=product["fields"]["updated_at"]
            )
            for product in products_data
        ]
        Product.objects.bulk_create(products_to_create)
