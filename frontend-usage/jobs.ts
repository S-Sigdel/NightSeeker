import { initJobsMiddleware } from './jobsMiddleware';
import { getWallet } from '@midnight-ntwrk/wallet';

async function setup() {
  const wallet = await getWallet();
  const config = { /* proof server, indexer, etc. */ };
  const jobs = await initJobsMiddleware(wallet, config);

  // Create a new job
  document.getElementById('createJobBtn').onclick = async () => {
    const commitment = /* generate commitment off-chain */;
    await jobs.createJob(commitment);
    alert('Job created!');
  };

  // Prove knowledge of a job
  document.getElementById('proveJobBtn').onclick = async () => {
    const jobId = /* get job ID from user input */;
    await jobs.proveJob(jobId);
    alert('Job proof submitted!');
  };
}
