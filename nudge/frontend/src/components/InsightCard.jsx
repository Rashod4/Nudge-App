const TYPE_STYLES = {
  overspending: {
    border: 'border-l-red-500',
    bg: 'bg-red-50',
    icon: '!',
    iconBg: 'bg-red-100 text-red-700',
  },
  warning: {
    border: 'border-l-amber-500',
    bg: 'bg-amber-50',
    icon: '!',
    iconBg: 'bg-amber-100 text-amber-700',
  },
  positive_trend: {
    border: 'border-l-emerald-500',
    bg: 'bg-emerald-50',
    icon: '\u2713',
    iconBg: 'bg-emerald-100 text-emerald-700',
  },
  recurring_alert: {
    border: 'border-l-blue-500',
    bg: 'bg-blue-50',
    icon: '\u21BB',
    iconBg: 'bg-blue-100 text-blue-700',
  },
};

const SUGGESTION_LABELS = {
  reduce: { text: 'Reduce', color: 'bg-red-100 text-red-700' },
  review: { text: 'Review', color: 'bg-amber-100 text-amber-700' },
  celebrate: { text: 'Nice!', color: 'bg-emerald-100 text-emerald-700' },
  monitor: { text: 'Monitor', color: 'bg-blue-100 text-blue-700' },
};

export default function InsightCard({ insight }) {
  const style = TYPE_STYLES[insight.type] || TYPE_STYLES.warning;
  const suggestion = SUGGESTION_LABELS[insight.suggestion_type] || SUGGESTION_LABELS.review;
  const confidencePct = Math.round(insight.confidence * 100);

  return (
    <div className={`border-l-4 ${style.border} ${style.bg} rounded-lg p-4 mb-3`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0 ${style.iconBg}`}>
            {style.icon}
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 text-sm">{insight.title}</h3>
            <p className="text-gray-600 text-sm mt-1">{insight.message}</p>
            <div className="flex items-center gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${suggestion.color}`}>
                {suggestion.text}
              </span>
              <span className="text-xs text-gray-400">
                {confidencePct}% confidence
              </span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                insight.source === 'ai'
                  ? 'bg-purple-100 text-purple-700'
                  : 'bg-gray-100 text-gray-600'
              }`}>
                {insight.source === 'ai' ? 'AI' : 'Rule-based'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
