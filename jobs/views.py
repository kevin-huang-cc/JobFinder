from rest_framework import generics
from django.http import JsonResponse
from .models import Job
from .serializers import JobSerializer
from jobs.google_scraper import GoogleJobScraper
import subprocess

# Filter for active jobs
def active_jobs(request):
    jobs = Job.objects.filter(status='active')
    job_list = list(jobs.values())
    return JsonResponse(job_list, safe=False)

# Filter for stashed jobs
def stashed_jobs(request):
    jobs = Job.objects.filter(status='stashed')
    job_list = list(jobs.values())
    return JsonResponse(job_list, safe=False)

# Mark job as stashed
def stash_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.status = 'stashed'
    job.save()
    return JsonResponse({'message': 'Job stashed successfully!'})

# Unstash a job (set status back to 'active')
def unstash_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.status = 'active'
        job.save()
        return JsonResponse({'message': 'Job unstashed successfully!'})
    except Job.DoesNotExist:
        return JsonResponse({'error': 'Job not found!'}, status=404)

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