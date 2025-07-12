import axios from 'axios';

const instance = axios.create({
//   baseURL: 'https://api.example.com', // Set your base URL
  timeout: 15000,
//   headers: {'X-Custom-Header': 'foobar'}
});

export default instance;
