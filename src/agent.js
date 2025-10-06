require('dotenv').config();
const os = require('os');
const axios = require('axios');

const SERVER_URL = process.env.SERVER_URL || 'http://localhost:3000';
const AGENT_ID = process.env.AGENT_ID || os.hostname();
const INTERVAL = parseInt(process.env.INTERVAL) || 30000; // 30 seconds

// Function to collect system metrics
function collectMetrics() {
  const metrics = {
    hostname: os.hostname(),
    platform: os.platform(),
    arch: os.arch(),
    uptime: os.uptime(),
    loadavg: os.loadavg(),
    totalmem: os.totalmem(),
    freemem: os.freemem(),
    cpus: os.cpus().length,
    cpuUsage: process.cpuUsage(),
  };

  return metrics;
}

// Function to send metrics to server
async function sendMetrics() {
  try {
    const metrics = collectMetrics();
    await axios.post(`${SERVER_URL}/api/metrics`, {
      agentId: AGENT_ID,
      data: metrics
    });
    console.log(`Metrics sent from ${AGENT_ID}`);
  } catch (error) {
    console.error('Failed to send metrics:', error.message);
  }
}

// Start collecting and sending metrics
console.log(`Starting Akij MonitorX agent ${AGENT_ID}`);
console.log(`Sending metrics to ${SERVER_URL} every ${INTERVAL / 1000} seconds`);

setInterval(sendMetrics, INTERVAL);

// Send initial metrics
sendMetrics();