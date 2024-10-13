import requests
from bs4 import BeautifulSoup
from jobs.models import Job

class GoogleJobScraper:
    def __init__(self):
        # Base URLs for scraping
        self.base_url = "https://www.google.com/about/careers/applications/jobs/results"
        self.learn_more_base_url = "https://www.google.com/about/careers/applications/"

    def scrape_google_jobs(self, page_num=1):
        url = f"{self.base_url}?page={page_num}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_num}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('li', class_='lLd3Je')

        jobs = []
        for card in job_cards:
            title_element = card.find('h3', class_='QJPWVe')
            title = title_element.get_text(strip=True) if title_element else 'N/A'

            learn_more_element = card.find('a', class_='WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb')
            learn_more_url = learn_more_element['href'] if learn_more_element else 'N/A'

            jobs.append({
                'title': title,
                'learn_more_url': learn_more_url,
            })
        return jobs

    def scrape_job_details(self, learn_more_url):
        url = f"{self.learn_more_base_url}{learn_more_url}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve job details from {url}")
            return {'location': 'N/A', 'experience_level': 'N/A'}

        soup = BeautifulSoup(response.text, 'html.parser')
        job_description = soup.find('div', class_='DkhPwc')

        location_element = job_description.find('span', class_='r0wTof')
        location = location_element.get_text(strip=True) if location_element else 'N/A'

        more_location = job_description.find('span', class_='BVHzed')
        more_locations = more_location.get_text(strip=True) if more_location else 'N/A'

        experience_element = job_description.find('span', class_='wVSTAb')
        experience_level = experience_element.get_text(strip=True) if experience_element else 'N/A'

        return {'location': location, 'more_locations': more_locations, 'experience_level': experience_level}

    def save_job(self, job_data):
            # Debugging: Find all jobs with the same learn_more_url
        matching_jobs = Job.objects.filter(learn_more_url=job_data['learn_more_url'])
    
        if matching_jobs.count() > 1:
            print("Multiple jobs found with the same learn_more_url:")
            for job in matching_jobs:
                print(f"ID: {job.id}, Title: {job.title}, URL: {job.learn_more_url}")

        Job.objects.update_or_create(
            learn_more_url = job_data['learn_more_url'], # Use URL for uniqueness
            defaults={
                'title': job_data['title'],
                'location': job_data['location'],
                'more_locations': job_data['more_locations'],
                'experience_level': job_data['experience_level'],
            }
        )

    def scrape_multiple_pages(self, num_pages):
        print(f"Received num_pages:{num_pages}")
        if num_pages <= 0:
            print("Invalid number of pages. Scraping 1 page by default.")
            num_pages = 1

        print(f"Page number is: {num_pages}")  # This should now print the correct value
    
        all_jobs = []
        for page in range(1, num_pages + 1):
            print(f"Scraping page {page}...")
            jobs = self.scrape_google_jobs(page)
            if jobs:
                for job in jobs:
                    details = self.scrape_job_details(job['learn_more_url'])
                    job.update(details)
                    self.save_job(job)
                all_jobs.extend(jobs)
        return all_jobs
