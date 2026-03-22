import { useState, useEffect } from 'react';
import { fetchSummary, fetchInsights, fetchTransactions, fetchCategories } from '../services/api';
import InsightsFeed from './InsightsFeed';
import SpendingChart from './SpendingChart';
import TransactionList from './TransactionList';

function SummaryCard({ label, value, sub, color = 'text-gray-900' }) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <p className="text-sm text-gray-500 font-medium">{label}</p>
      <p className={`text-2xl font-bold mt-1 ${color}`}>{value}</p>
      {sub && <p className="text-xs text-gray-400 mt-1">{sub}</p>}
    </div>
  );
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [insightsData, setInsightsData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

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
      } catch (err) {
        console.error('Failed to load data:', err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const insights = insightsData?.insights || [];
  const aiAvailable = insightsData?.ai_available ?? false;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-5">
          <h1 className="text-2xl font-bold text-gray-900">Nudge</h1>
          <p className="text-sm text-gray-500 mt-0.5">Financial Intelligence Engine</p>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6 space-y-6">
        {/* Summary Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <SummaryCard
            label="Total Spent"
            value={summary ? `$${summary.total_spent.toLocaleString()}` : '...'}
            sub={summary ? `over ${summary.days_of_data} days` : ''}
            color="text-gray-900"
          />
          <SummaryCard
            label="Income"
            value={summary ? `$${summary.total_income.toLocaleString()}` : '...'}
            color="text-emerald-600"
          />
          <SummaryCard
            label="Daily Burn Rate"
            value={summary ? `$${summary.burn_rate_daily}/day` : '...'}
            sub={summary ? `~$${(summary.burn_rate_daily * 30).toFixed(0)}/mo projected` : ''}
            color="text-amber-600"
          />
          <SummaryCard
            label="Active Insights"
            value={loading ? '...' : insights.length}
            sub={aiAvailable ? 'AI + Rule engine' : 'Rule engine only'}
          />
        </div>

        {/* Insights + Chart */}
        <div className="grid lg:grid-cols-5 gap-6">
          <div className="lg:col-span-3 bg-white rounded-xl border border-gray-200 p-5">
            <InsightsFeed
              insights={insights}
              aiAvailable={aiAvailable}
              loading={loading}
            />
          </div>
          <div className="lg:col-span-2 bg-white rounded-xl border border-gray-200 p-5">
            <SpendingChart
              breakdown={summary?.category_breakdown || []}
              loading={loading}
            />
          </div>
        </div>

        {/* Transactions */}
        <div className="bg-white rounded-xl border border-gray-200 p-5">
          <TransactionList
            transactions={transactions}
            categories={categories}
            loading={loading}
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-8">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-400">
          Nudge v1.0 — AI responses validated with Pydantic schemas. Rule engine runs deterministically.
        </div>
      </footer>
    </div>
  );
}
