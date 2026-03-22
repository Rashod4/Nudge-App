import { useState } from 'react';

const CATEGORY_COLORS = {
  food: 'bg-orange-100 text-orange-700',
  rent: 'bg-red-100 text-red-700',
  utilities: 'bg-indigo-100 text-indigo-700',
  entertainment: 'bg-pink-100 text-pink-700',
  transportation: 'bg-blue-100 text-blue-700',
  shopping: 'bg-yellow-100 text-yellow-700',
  subscription: 'bg-purple-100 text-purple-700',
  income: 'bg-emerald-100 text-emerald-700',
  transfer: 'bg-gray-100 text-gray-600',
  uncategorized: 'bg-gray-100 text-gray-500',
};

export default function TransactionList({ transactions, categories, loading }) {
  const [filter, setFilter] = useState('all');
  const [showAll, setShowAll] = useState(false);

  if (loading) {
    return (
      <div className="space-y-2">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="bg-gray-100 rounded h-10 animate-pulse" />
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
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Recent Transactions</h2>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="text-sm border border-gray-300 rounded-md px-2 py-1 bg-white"
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
            <tr className="border-b border-gray-200 text-left text-gray-500">
              <th className="pb-2 font-medium">Date</th>
              <th className="pb-2 font-medium">Description</th>
              <th className="pb-2 font-medium">Category</th>
              <th className="pb-2 font-medium text-right">Amount</th>
            </tr>
          </thead>
          <tbody>
            {displayed.map((txn) => (
              <tr key={txn.id} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-2.5 text-gray-600 whitespace-nowrap">
                  {new Date(txn.date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </td>
                <td className="py-2.5 text-gray-900 font-medium truncate max-w-[200px]">
                  {txn.raw_description}
                </td>
                <td className="py-2.5">
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${CATEGORY_COLORS[txn.category] || CATEGORY_COLORS.uncategorized}`}>
                    {txn.category}
                  </span>
                </td>
                <td className={`py-2.5 text-right font-mono font-medium ${txn.amount > 0 ? 'text-emerald-600' : 'text-gray-900'}`}>
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
          className="mt-3 text-sm text-blue-600 hover:text-blue-700 font-medium"
        >
          Show all {filtered.length} transactions
        </button>
      )}
    </div>
  );
}
