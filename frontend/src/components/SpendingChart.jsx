import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const CATEGORY_COLORS = {
  rent: '#ef4444',
  food: '#f97316',
  shopping: '#eab308',
  utilities: '#6366f1',
  transportation: '#3b82f6',
  subscription: '#8b5cf6',
  entertainment: '#ec4899',
  transfer: '#6b7280',
  uncategorized: '#9ca3af',
};

export default function SpendingChart({ breakdown, loading }) {
  if (loading) {
    return <div className="bg-gray-100 rounded-lg h-64 animate-pulse" />;
  }

  if (!breakdown || breakdown.length === 0) {
    return <p className="text-gray-500 text-sm">No spending data.</p>;
  }

  // Exclude income from chart
  const data = breakdown
    .filter((c) => c.category !== 'income')
    .map((c) => ({
      name: c.category.charAt(0).toUpperCase() + c.category.slice(1),
      amount: c.total,
      category: c.category,
    }));

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Spending by Category</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical" margin={{ left: 80, right: 20, top: 5, bottom: 5 }}>
          <XAxis type="number" tickFormatter={(v) => `$${v}`} />
          <YAxis type="category" dataKey="name" width={80} tick={{ fontSize: 12 }} />
          <Tooltip
            formatter={(value) => [`$${value.toFixed(2)}`, 'Amount']}
            contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
          />
          <Bar dataKey="amount" radius={[0, 4, 4, 0]}>
            {data.map((entry) => (
              <Cell key={entry.category} fill={CATEGORY_COLORS[entry.category] || '#9ca3af'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
