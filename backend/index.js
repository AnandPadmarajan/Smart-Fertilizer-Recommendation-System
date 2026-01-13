const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.json());

// Route that calls your FastAPI service
app.post('/recommend', async (req, res) => {
  console.log('Incoming request:', req.body);
  try {
    const response = await axios.post(
      'https://smart-fertilizer-recommendation-system.onrender.com/recommend',
      req.body
    );
    console.log('Response from FastAPI:', response.data);
    res.json(response.data);
  } catch (err) {
    console.error('Error calling FastAPI:', err.message);
    res.status(500).json({ error: 'Failed to get recommendation' });
  }
});

app.get('/health', async (req, res) => {
  try {
    const response = await axios.get(
      'https://smart-fertilizer-recommendation-system.onrender.com/health'
    );
    res.json({ backend: 'ok', fastapi: response.data.status });
  } catch (err) {
    res.json({ backend: 'ok', fastapi: 'down' });
  }
});

app.listen(3000, () => {
  console.log('Node backend running on port 3000');
});