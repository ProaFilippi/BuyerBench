interface ScoreBarProps {
  score: number;
  color: string;
  showLabel?: boolean;
}

export default function ScoreBar({ score, color, showLabel = true }: ScoreBarProps) {
  const pct = Math.round(score * 100);
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
      <div
        className="brutal-border"
        style={{
          position: 'relative',
          height: '20px',
          flex: 1,
          background: 'rgba(10,10,10,0.06)',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: 0,
            height: '100%',
            width: `${pct}%`,
            background: color,
            transition: 'width 0.3s ease',
            opacity: 0.85,
          }}
        />
      </div>
      {showLabel && (
        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.72rem',
            fontWeight: 700,
            whiteSpace: 'nowrap',
            minWidth: '3ch',
            textAlign: 'right',
          }}
        >
          {pct}%
        </span>
      )}
    </div>
  );
}
