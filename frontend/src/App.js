import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false)


  const fetchJobs = () => {
    setLoading(true);
    axios.get('http://localhost:8000/api/jobs/')
    .then(response => {
      // console.log('Fetched jobs:', response.data)
      setJobs(response.data);
      setLoading(false);
    })
    .catch(error => {
      console.error('There was an error fetching the jobs!', error);
      setLoading(false)
    });
  }

  const runScraper = () => {
    setLoading(true);
    axios.get('http://localhost:8000/api/scrape/')
      .then(response => {
        console.log(response.data.message);
        fetchJobs();
      })
      .catch(error => {
        console.error('Error runing scraper:', error)
        setLoading(false)
      })
  }
  // Fetch jobs from the Django backend API
  useEffect(() => {
      fetchJobs();
  }, []);

  return (
    <div className="App">
      <h1>Job Listings</h1>
      <button className="refresh-button" onClick={runScraper} disabled={loading}>
        {loading ? 'Refreshing...':'Refresh Jobs'}
      </button>
      <div className="job-cards">
        {jobs.map(job => (
          <div key={job.id} className="job-card">
            <h2>{job.title}</h2>
            <p><strong>Location:</strong> {job.location || 'N/A'}</p>
            <p><strong>Experience Level:</strong> {job.experience_level || 'N/A'}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
