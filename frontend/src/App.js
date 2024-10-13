import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false)
  const [view, setView] = useState('active'); // Track active or stashed view


  const fetchJobs = (type = 'active') => {
    setLoading(true);
    axios.get(`http://localhost:8000/api/${type}/`)
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

  // Mark job as stashed
  const stashJob = (jobId) => {
    axios.get(`http://localhost:8000/api/stash/${jobId}/`)
      .then(response => {
        console.log(response.data.message);
        fetchJobs(view); // Refresh the current view
      })
      .catch(error => {
        console.error('Error stashing job:', error);
      });
  };

  // Unstash a job (move it back to active view)
  const unstashJob = (jobId) => {
    axios.get(`http://localhost:8000/api/unstash/${jobId}/`)
      .then(response => {
        console.log(response.data.message);
        fetchJobs(view); // Refresh the current view
      })
      .catch(error => {
        console.error('Error unstashing job:', error);
      });
  };

  // Fetch jobs from the Django backend API
  useEffect(() => {
      fetchJobs(view);
  }, [view]);

  return (
    <div className="App">
      <h1>Job Listings</h1>
      <div className="view-buttons">
        <button onClick={() => setView('active')} disabled={view === 'active'}>
          Active Jobs
        </button>
        <button onClick={() => setView('stashed')} disabled={view === 'stashed'}>
          Stashed Jobs
        </button>
      </div>
      <button className="refresh-button" onClick={runScraper} disabled={loading}>
        {loading ? 'Refreshing...' : 'Refresh Jobs'}
      </button>
      <div className="job-cards">
        {jobs.map(job => (
          <div key={job.id} className="job-card">
            <h2>{job.title}</h2>
            <p><strong>Location:</strong> {job.location || 'N/A'}</p>
            <p><strong>Experience Level:</strong> {job.experience_level || 'N/A'}</p>
            {view === 'active' ? (
              <button onClick={() => stashJob(job.id)}>
                Stash Job
              </button>
            ) : (
              <button onClick={() => unstashJob(job.id)}>
                Unstash Job
              </button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}


export default App;
