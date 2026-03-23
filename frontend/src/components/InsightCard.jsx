const TYPE_STYLES = {
  overspending: {
    border: 'border-l-danger',
    iconBg: 'bg-danger/15 text-danger',
    icon: '\u2193',
  },
  warning: {
    border: 'border-l-warning',
    iconBg: 'bg-warning/15 text-warning',
    icon: '\u26A0',
  },
  positive_trend: {
    border: 'border-l-positive',
    iconBg: 'bg-positive/15 text-positive',
    icon: '\u2191',
  },
  recurring_alert: {
    border: 'border-l-info',
    iconBg: 'bg-info/15 text-info',
    icon: '\u21BB',
  },
};

const SUGGESTION_LABELS = {
  reduce: { text: 'Reduce', color: 'bg-danger/15 text-danger' },
  review: { text: 'Review', color: 'bg-warning/15 text-warning' },
  celebrate: { text: 'Nice!', color: 'bg-positive/15 text-positive' },
  monitor: { text: 'Monitor', color: 'bg-info/15 text-info' },
};

export default function InsightCard({ insight, index }) {
  const style = TYPE_STYLES[insight.type] || TYPE_STYLES.warning;
  const suggestion = SUGGESTION_LABELS[insight.suggestion_type] || SUGGESTION_LABELS.review;
  const confidencePct = Math.round(insight.confidence * 100);

  return (
    <div
      className={`border-l-3 ${style.border} bg-surface-overlay rounded-xl p-4 hover:bg-surface-overlay/80 transition-all duration-200 animate-fade-in-up`}
      style={{ animationDelay: `${index * 60}ms` }}
    >
      <div className="flex items-start gap-3">
        <div className={`w-9 h-9 rounded-lg flex items-center justify-center text-sm font-bold shrink-0 ${style.iconBg}`}>
          {style.icon}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-text-primary text-sm leading-snug">{insight.title}</h3>
          <p className="text-text-secondary text-sm mt-1 leading-relaxed">{insight.message}</p>
          <div className="flex flex-wrap items-center gap-2 mt-3">
            <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${suggestion.color}`}>
              {suggestion.text}
            </span>
            <span className="text-xs text-text-muted">
              {confidencePct}%
            </span>
            <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${
              insight.source === 'ai'
                ? 'bg-accent/15 text-accent-light'
                : 'bg-surface-raised text-text-muted'
            }`}>
              {insight.source === 'ai' ? 'AI' : 'Rule'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
