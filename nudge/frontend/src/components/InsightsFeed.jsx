import InsightCard from './InsightCard';

export default function InsightsFeed({ insights, aiAvailable, loading }) {
  if (loading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-gray-100 rounded-lg h-24 animate-pulse" />
        ))}
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Insights</h2>
        {!aiAvailable && (
          <span className="text-xs px-2 py-1 bg-amber-100 text-amber-700 rounded-full">
            Rule-based only
          </span>
        )}
      </div>
      {insights.length === 0 ? (
        <p className="text-gray-500 text-sm">No insights available yet.</p>
      ) : (
        insights.map((insight, idx) => (
          <InsightCard key={idx} insight={insight} />
        ))
      )}
    </div>
  );
}
