const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const log = (msg, ...args) => {
  console.log('[Ghost API]', msg, ...args);
};

export async function scanEmails() {
  const url = `${API_URL}/api/scan`;
  log('scanEmails: requesting', url);
  try {
    const response = await fetch(url);
    log('scanEmails: got response', { status: response.status, statusText: response.statusText, ok: response.ok, headers: Object.fromEntries(response.headers.entries()) });
    if (!response.ok) {
      const text = await response.text();
      log('scanEmails: non-OK body', text);
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    const data = await response.json();
    log('scanEmails: parsed JSON', { success: data.success, serviceCount: data.services?.length });
    return data;
  } catch (err) {
    log('scanEmails: fetch failed', err.name, err.message, err.cause ?? '', err.stack);
    throw err;
  }
}

export async function healthCheck() {
  const url = `${API_URL}/health`;
  log('healthCheck: requesting', url);
  try {
    const response = await fetch(url);
    log('healthCheck: got response', { status: response.status, ok: response.ok });
    if (!response.ok) throw new Error('API error');
    return response.json();
  } catch (err) {
    log('healthCheck: fetch failed', err.name, err.message, err.cause ?? '', err.stack);
    throw err;
  }
}
