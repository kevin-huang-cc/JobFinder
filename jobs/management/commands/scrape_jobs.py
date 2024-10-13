from django.core.management.base import BaseCommand
from jobs.google_scraper import GoogleJobScraper  # Import the scraper

class Command(BaseCommand):
    help = 'Scrape jobs from Google Careers and store them in the database'

    def handle(self, *args, **kwargs):
        scraper = GoogleJobScraper()
        value_ = 2
        scraper.scrape_multiple_pages(num_pages=value_)

        self.stdout.write(self.style.SUCCESS('Successfully scraped and stored jobs!'))
