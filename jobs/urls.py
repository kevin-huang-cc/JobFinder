from django.urls import path
from .views import JobList, JobDetail, run_scraper

urlpatterns = [
    path('jobs/', JobList.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'), # View specific job with id
    path('scrape/', run_scraper, name='run_scraper'), # Scraper trigger endpoint
]

