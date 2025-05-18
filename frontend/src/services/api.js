// frontend/src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Certifique-se de que seu FastAPI está rodando nesta porta
  headers: {
    'Content-Type': 'application/json'
  }
});

export default api;
