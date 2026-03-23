import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const CATEGORY_COLORS = {
  rent: '#ff7675',
  food: '#fdcb6e',
  shopping: '#fab1a0',
  utilities: '#a29bfe',
  transportation: '#74b9ff',
  subscription: '#6c5ce7',
  entertainment: '#fd79a8',
  transfer: '#636e72',
  uncategorized: '#b2bec3',
};

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-surface-overlay border border-border rounded-lg px-3 py-2 shadow-lg">
      <p className="text-xs text-text-muted">{payload[0].payload.name}</p>
      <p className="text-sm font-semibold text-text-primary">${payload[0].value.toFixed(2)}</p>
    </div>
  );
};

export default function SpendingChart({ breakdown, loading }) {
  if (loading) {
    return <div className="skeleton rounded-xl h-72" />;
  }

  if (!breakdown || breakdown.length === 0) {
    return <p className="text-text-muted text-sm">No spending data.</p>;
  }

  const data = breakdown
    .filter((c) => c.category !== 'income')
    .map((c) => ({
      name: c.category.charAt(0).toUpperCase() + c.category.slice(1),
      amount: c.total,
      category: c.category,
    }))
    .sort((a, b) => b.amount - a.amount);

  return (
    <div>
      <h2 className="text-base font-semibold text-text-primary mb-5">Spending by Category</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="vertical" margin={{ left: 0, right: 10, top: 0, bottom: 0 }}>
          <XAxis
            type="number"
            tickFormatter={(v) => `$${v}`}
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#5c6178', fontSize: 11 }}
          />
          <YAxis
            type="category"
            dataKey="name"
            width={90}
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#9196ab', fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <Bar dataKey="amount" radius={[0, 6, 6, 0]} barSize={20}>
            {data.map((entry) => (
              <Cell key={entry.category} fill={CATEGORY_COLORS[entry.category] || '#b2bec3'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
