from django.core.management.base import BaseCommand
from jobs.google_scraper import GoogleJobScraper  # Import the scraper

class Command(BaseCommand):
    help = 'Scrape jobs from Google Careers and store them in the database'

    def handle(self, *args, **kwargs):
        print("Starting handle method")
        scraper = GoogleJobScraper()
        value_ = 3
        print(f"Calling scrape_multiple_pages with num_pages={value_}")
        scraper.scrape_multiple_pages(num_pages=value_)  # Scrape 1 page

        self.stdout.write(self.style.SUCCESS('Successfully scraped and stored jobs!'))
