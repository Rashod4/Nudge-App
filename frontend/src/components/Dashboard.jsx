import { useState, useEffect } from 'react';
import { fetchSummary, fetchInsights, fetchAiInsights, fetchTransactions, fetchCategories } from '../services/api';
import InsightsFeed from './InsightsFeed';
import SpendingChart from './SpendingChart';
import TransactionList from './TransactionList';

function SummaryCard({ label, value, sub, icon, accent = 'text-text-primary' }) {
  return (
    <div className="bg-surface-raised border border-border rounded-2xl p-5 hover:border-border/80 transition-all duration-200 animate-fade-in-up">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-lg">{icon}</span>
        <p className="text-xs font-medium text-text-muted uppercase tracking-wider">{label}</p>
      </div>
      <p className={`text-2xl font-bold ${accent}`}>{value}</p>
      {sub && <p className="text-xs text-text-muted mt-2">{sub}</p>}
    </div>
  );
}

function AiStatusPill({ aiLoading, aiAvailable }) {
  if (aiLoading) {
    return (
      <span className="inline-flex items-center gap-1.5 text-xs px-3 py-1 rounded-full bg-accent/10 text-accent-light">
        <span className="w-1.5 h-1.5 rounded-full bg-accent-light animate-pulse" />
        AI analyzing...
      </span>
    );
  }
  if (aiAvailable) {
    return (
      <span className="inline-flex items-center gap-1.5 text-xs px-3 py-1 rounded-full bg-positive/10 text-positive">
        <span className="w-1.5 h-1.5 rounded-full bg-positive" />
        AI + Rules
      </span>
    );
  }
  return (
    <span className="inline-flex items-center gap-1.5 text-xs px-3 py-1 rounded-full bg-warning/10 text-warning">
      <span className="w-1.5 h-1.5 rounded-full bg-warning" />
      Rules only
    </span>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [insightsData, setInsightsData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [sum, ins, txns, cats] = await Promise.all([
          fetchSummary(),
          fetchInsights(),
          fetchTransactions(),
          fetchCategories(),
        ]);
        setSummary(sum);
        setInsightsData(ins);
        setTransactions(txns);
        setCategories(cats);
        setLoading(false);

        try {
          const aiIns = await fetchAiInsights();
          setInsightsData(aiIns);
        } catch (err) {
          console.error('AI insights failed:', err);
        } finally {
          setAiLoading(false);
        }
      } catch (err) {
        console.error('Failed to load data:', err);
        setLoading(false);
        setAiLoading(false);
      }
    }
    load();
  }, []);

  const insights = insightsData?.insights || [];
  const aiAvailable = insightsData?.ai_available ?? false;

  return (
    <div className="min-h-screen bg-surface">
      {/* Header */}
      <header className="border-b border-border bg-surface-raised/50 backdrop-blur-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-accent to-accent-light flex items-center justify-center text-white font-bold text-sm">
              N
            </div>
            <div>
              <h1 className="text-lg font-bold text-text-primary">Nudge</h1>
              <p className="text-xs text-text-muted">Financial Intelligence</p>
            </div>
          </div>
          <AiStatusPill aiLoading={aiLoading} aiAvailable={aiAvailable} />
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <SummaryCard
            icon="$"
            label="Total Spent"
            value={summary ? `$${summary.total_spent.toLocaleString()}` : '...'}
            sub={summary ? `over ${summary.days_of_data} days` : ''}
          />
          <SummaryCard
            icon="+"
            label="Income"
            value={summary ? `$${summary.total_income.toLocaleString()}` : '...'}
            accent="text-positive"
          />
          <SummaryCard
            icon="~"
            label="Burn Rate"
            value={summary ? `$${summary.burn_rate_daily}/day` : '...'}
            sub={summary ? `~$${(summary.burn_rate_daily * 30).toFixed(0)}/mo projected` : ''}
            accent="text-warning"
          />
          <SummaryCard
            icon="#"
            label="Insights"
            value={loading ? '...' : insights.length}
            sub={aiLoading ? 'Loading AI insights...' : aiAvailable ? 'AI + Rule engine' : 'Rule engine only'}
            accent="text-accent-light"
          />
        </div>

        {/* Insights + Chart */}
        <div className="grid lg:grid-cols-5 gap-6">
          <div className="lg:col-span-3 bg-surface-raised border border-border rounded-2xl p-6">
            <InsightsFeed
              insights={insights}
              aiAvailable={aiAvailable}
              aiLoading={aiLoading}
              loading={loading}
            />
          </div>
          <div className="lg:col-span-2 bg-surface-raised border border-border rounded-2xl p-6">
            <SpendingChart
              breakdown={summary?.category_breakdown || []}
              loading={loading}
            />
          </div>
        </div>

        {/* Transactions */}
        <div className="bg-surface-raised border border-border rounded-2xl p-6">
          <TransactionList
            transactions={transactions}
            categories={categories}
            loading={loading}
          />
        </div>
      </main>

      <footer className="border-t border-border mt-4">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-xs text-text-muted">
          Nudge v1.0 — AI insights validated with Pydantic. Rule engine runs deterministically.
        </div>
      </footer>
    </div>
  );
}
