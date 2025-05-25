# your_app/management/commands/seed_domains.py

import csv
import os
from django.core.management.base import BaseCommand
from main.models import domain, Category

class Command(BaseCommand):
    help = 'Seed domains from the Majestic Million CSV'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..', 'majestic_million.csv')
        file_path = os.path.normpath(file_path)

        if not os.path.exists(file_path):
            self.stderr.write(f"CSV file not found at {file_path}")
            return

        try:
            category = Category.objects.get(pk=2)
        except Category.DoesNotExist:
            self.stderr.write("Category with ID=2 does not exist.")
            return

        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                csvDomain = row.get('Domain')
                if csvDomain:
                    domain.objects.get_or_create(name=csvDomain.strip(), category=category)
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} domains'))
