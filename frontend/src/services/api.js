const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function scanEmails() {
  const response = await fetch(`${API_URL}/api/scan`);
  if (!response.ok) throw new Error('API error');
  return response.json();
}

export async function healthCheck() {
  const response = await fetch(`${API_URL}/health`);
  if (!response.ok) throw new Error('API error');
  return response.json();
}
