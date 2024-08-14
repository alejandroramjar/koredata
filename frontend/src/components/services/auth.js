import axios from 'axios';

export async function isAuthenticated() {
  const token = localStorage.getItem('token');
  if (!token) {
    return false;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/token/verify/', { token });
    return response.status === 200;
  } catch (error) {
    console.error('Token inválido:', error);
    return false;
  }
}
