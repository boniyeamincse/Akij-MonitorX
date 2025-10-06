require('dotenv').config();
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const PORT = process.env.PORT || 3000;

// In-memory storage for metrics (for simplicity)
let metrics = {};

// Middleware
app.use(express.json());
// Serve static files from the project's top-level `public` folder
app.use(express.static(path.join(__dirname, '..', 'public')));

// API endpoint to receive metrics from agents
app.post('/api/metrics', (req, res) => {
  const { agentId, data } = req.body;
  metrics[agentId] = { ...data, timestamp: new Date() };
  console.log(`Received metrics from ${agentId}:`, data);

  // Emit to connected clients
  io.emit('metricsUpdate', { agentId, data: metrics[agentId] });

  res.json({ status: 'ok' });
});

// API endpoint to get all metrics
app.get('/api/metrics', (req, res) => {
  res.json(metrics);
});

// Dashboard route - resolve to the top-level public/index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '..', 'public', 'index.html'));
});

// Socket.io for real-time updates
io.on('connection', (socket) => {
  console.log('Client connected');
  socket.emit('initialMetrics', metrics);

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(PORT, () => {
  console.log(`Akij MonitorX server running on port ${PORT}`);
});