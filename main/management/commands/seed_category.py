from django.core.management.base import BaseCommand
from main.models import Category

class Command(BaseCommand):
    help = 'Seed initial categories (Spam, Legitimate)'

    def handle(self, *args, **kwargs):
        data = [
            {"id": 1, "name": "Spam"},
            {"id": 2, "name": "Legitimate"},
        ]
        for item in data:
            obj, created = Category.objects.get_or_create(id=item["id"], defaults={"name": item["name"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Category: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {obj.name}"))
