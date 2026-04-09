import type { PillarAggregate } from '@/types/report';

interface ScenarioCountProps {
  pillarAggregates: PillarAggregate[];
}

const PILLARS = [
  { key: 'PILLAR1', label: 'PILLAR 1 — CAPABILITY',   color: 'var(--accent)' },
  { key: 'PILLAR2', label: 'PILLAR 2 — ECONOMICS',    color: '#e6c700' },
  { key: 'PILLAR3', label: 'PILLAR 3 — SECURITY',     color: 'var(--accent3)' },
] as const;

function maxScenariosForPillar(aggregates: PillarAggregate[], pillar: string): number {
  const rows = aggregates.filter((r) => r.pillar === pillar);
  if (rows.length === 0) return 0;
  return Math.max(...rows.map((r) => r.n_scenarios));
}

export default function ScenarioCount({ pillarAggregates }: ScenarioCountProps) {
  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '1rem',
      }}
    >
      {PILLARS.map(({ key, label, color }) => {
        const count = maxScenariosForPillar(pillarAggregates, key);
        return (
          <div
            key={key}
            className="brutal-box"
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'flex-start',
              gap: '0.4rem',
              borderLeft: `6px solid ${color}`,
              padding: '1.25rem 1.5rem',
            }}
          >
            <span
              style={{
                fontFamily: 'var(--font-sans)',
                fontSize: 'clamp(2rem, 4vw, 2.75rem)',
                fontWeight: 900,
                lineHeight: 1,
                color,
              }}
            >
              {count}
            </span>
            <span
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.7rem',
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                fontWeight: 600,
                opacity: 0.75,
              }}
            >
              {label}
            </span>
            <span
              style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.65rem',
                opacity: 0.5,
                letterSpacing: '0.05em',
              }}
            >
              SCENARIOS
            </span>
          </div>
        );
      })}
    </div>
  );
}
