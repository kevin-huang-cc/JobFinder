from rest_framework import generics
from django.http import JsonResponse
from .models import Job
from .serializers import JobSerializer
from jobs.google_scraper import GoogleJobScraper
import subprocess

# List and Create Jobs
class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    def get(self, request, *args, **kwargs):
        print("Jobs retrieved from database:", list(Job.objects.values()))
        return self.list(request, *args, **kwargs)

# Retrieve, Update, and Delete a Single Job
class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# API Endpoint that Uses the Management Command
def run_scraper(request):
    try:
        # Call the management command from the API endpoint
        result = subprocess.run(['python', 'manage.py', 'scrape_jobs'], capture_output=True, text=True)

        if result.returncode == 0:
            return JsonResponse({'message': 'Scraper executed successfully!'})
        else:
            return JsonResponse({'error': result.stderr}, status=500)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)