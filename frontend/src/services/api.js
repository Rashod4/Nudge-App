const BASE = '/api';

export async function fetchTransactions(category = null) {
  const params = new URLSearchParams();
  if (category) params.set('category', category);
  const res = await fetch(`${BASE}/transactions?${params}`);
  return res.json();
}

export async function fetchInsights() {
  const res = await fetch(`${BASE}/insights`);
  return res.json();
}

export async function fetchAiInsights() {
  const res = await fetch(`${BASE}/insights/ai`);
  return res.json();
}

export async function fetchSummary(timeframe = 'all') {
  const res = await fetch(`${BASE}/summary?timeframe=${timeframe}`);
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${BASE}/categories`);
  return res.json();
}
