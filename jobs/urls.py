from django.urls import path
from .views import JobList, JobDetail, run_scraper, active_jobs, stashed_jobs, stash_job, unstash_job

urlpatterns = [
    #path('jobs/', JobList.as_view(), name='job-list'),
    #path('jobs/<int:pk>/', JobDetail.as_view(), name='job-detail'), # View specific job with id
    path('scrape/', run_scraper, name='run_scraper'), # Scraper trigger endpoint
    path('active/', active_jobs, name='active_jobs'),
    path('stashed/', stashed_jobs, name='stashed_jobs'),
    path('stash/<int:job_id>/', stash_job, name='stash_job'),
    path('unstash/<int:job_id>/', unstash_job, name='unstash_job'),

]

