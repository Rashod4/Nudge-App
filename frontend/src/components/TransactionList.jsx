import { useState } from 'react';

const CATEGORY_COLORS = {
  food: 'bg-warning/15 text-warning',
  rent: 'bg-danger/15 text-danger',
  utilities: 'bg-accent/15 text-accent-light',
  entertainment: 'bg-pink-500/15 text-pink-400',
  transportation: 'bg-info/15 text-info',
  shopping: 'bg-orange-500/15 text-orange-400',
  subscription: 'bg-accent/15 text-accent-light',
  income: 'bg-positive/15 text-positive',
  transfer: 'bg-surface-overlay text-text-muted',
  uncategorized: 'bg-surface-overlay text-text-muted',
};

export default function TransactionList({ transactions, categories, loading }) {
  const [filter, setFilter] = useState('all');
  const [showAll, setShowAll] = useState(false);

  if (loading) {
    return (
      <div className="space-y-2">
        <div className="h-5 w-40 skeleton rounded mb-4" />
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="skeleton rounded-lg h-12" />
        ))}
      </div>
    );
  }

  const filtered = filter === 'all'
    ? transactions
    : transactions.filter((t) => t.category === filter);

  const displayed = showAll ? filtered : filtered.slice(0, 20);

  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-base font-semibold text-text-primary">Transactions</h2>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="text-sm bg-surface-overlay border border-border text-text-secondary rounded-lg px-3 py-1.5 focus:outline-none focus:border-accent transition-colors"
        >
          <option value="all">All Categories</option>
          {categories.map((c) => (
            <option key={c.name} value={c.name}>{c.label}</option>
          ))}
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left">
              <th className="pb-3 text-xs font-medium text-text-muted uppercase tracking-wider">Date</th>
              <th className="pb-3 text-xs font-medium text-text-muted uppercase tracking-wider">Description</th>
              <th className="pb-3 text-xs font-medium text-text-muted uppercase tracking-wider">Category</th>
              <th className="pb-3 text-xs font-medium text-text-muted uppercase tracking-wider text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {displayed.map((txn, idx) => (
              <tr
                key={txn.id}
                className="border-b border-border-subtle hover:bg-surface-overlay/50 transition-colors animate-fade-in-up"
                style={{ animationDelay: `${idx * 20}ms` }}
              >
                <td className="py-3 text-text-muted whitespace-nowrap">
                  {new Date(txn.date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </td>
                <td className="py-3 text-text-primary font-medium truncate max-w-[250px]">
                  {txn.raw_description}
                </td>
                <td className="py-3">
                  <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${CATEGORY_COLORS[txn.category] || CATEGORY_COLORS.uncategorized}`}>
                    {txn.category}
                  </span>
                </td>
                <td className={`py-3 text-right font-mono font-medium ${txn.amount > 0 ? 'text-positive' : 'text-text-primary'}`}>
                  {txn.amount > 0 ? '+' : ''}{txn.amount < 0 ? '-' : ''}${Math.abs(txn.amount).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filtered.length > 20 && !showAll && (
        <button
          onClick={() => setShowAll(true)}
          className="mt-4 text-sm text-accent-light hover:text-accent font-medium transition-colors"
        >
          Show all {filtered.length} transactions
        </button>
      )}
    </div>
  );
}
