import InsightCard from './InsightCard';

export default function InsightsFeed({ insights, aiAvailable, aiLoading, loading }) {
  if (loading) {
    return (
      <div className="space-y-3">
        <div className="h-5 w-24 skeleton rounded mb-4" />
        {[1, 2, 3].map((i) => (
          <div key={i} className="skeleton rounded-xl h-28" />
        ))}
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-base font-semibold text-text-primary">Insights</h2>
        {aiLoading && (
          <span className="text-xs px-2.5 py-1 rounded-full bg-accent/10 text-accent-light animate-pulse">
            Loading AI...
          </span>
        )}
      </div>
      {insights.length === 0 ? (
        <p className="text-text-muted text-sm">No insights available yet.</p>
      ) : (
        <div className="space-y-3">
          {insights.map((insight, idx) => (
            <InsightCard key={idx} insight={insight} index={idx} />
          ))}
        </div>
      )}
    </div>
  );
}
