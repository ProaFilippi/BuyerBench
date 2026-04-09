import type { AgentSummary } from '@/types/report';

interface AgentHeaderProps {
  agentId: string;
  summary: AgentSummary | undefined;
}

function formatAgentId(id: string): string {
  if (id.startsWith('openrouter-')) {
    const parts = id.replace('openrouter-', '').split('-');
    parts[0] = parts[0].toUpperCase();
    return parts.join(' ');
  }
  return id.replace(/-/g, ' ');
}

function PillarBadge({ label, score, color }: { label: string; score: number | null; color: string }) {
  return (
    <div
      style={{
        display: 'inline-flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '0.2rem',
        padding: '0.4rem 0.9rem',
        border: '2px solid var(--fg)',
        background: score !== null ? color : 'transparent',
        minWidth: '80px',
      }}
    >
      <span
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.65rem',
          fontWeight: 700,
          letterSpacing: '0.1em',
          color: score !== null ? 'var(--fg)' : 'rgba(10,10,10,0.4)',
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '1.1rem',
          fontWeight: 700,
          color: score !== null ? 'var(--fg)' : 'rgba(10,10,10,0.4)',
        }}
      >
        {score !== null ? `${Math.round(score * 100)}%` : 'N/A'}
      </span>
    </div>
  );
}

export default function AgentHeader({ agentId, summary }: AgentHeaderProps) {
  const overall = summary?.overall_score ?? null;

  return (
    <div style={{ paddingBottom: '2rem', borderBottom: 'var(--border)', marginBottom: '2rem' }}>
      <p
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.72rem',
          letterSpacing: '0.12em',
          opacity: 0.5,
          marginBottom: '0.5rem',
          textTransform: 'uppercase',
        }}
      >
        AGENT PROFILE
      </p>
      <h1
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: 'clamp(1.2rem, 3vw, 2rem)',
          fontWeight: 700,
          letterSpacing: '-0.01em',
          marginBottom: '1.5rem',
          wordBreak: 'break-all',
        }}
      >
        {formatAgentId(agentId)}
      </h1>

      <div style={{ display: 'flex', alignItems: 'flex-end', gap: '2rem', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
          <PillarBadge label="P1 CAPABILITY" score={summary?.pillar1_score ?? null} color="rgba(255,59,0,0.18)" />
          <PillarBadge label="P2 ECONOMICS"  score={summary?.pillar2_score ?? null} color="rgba(230,199,0,0.35)" />
          <PillarBadge label="P3 SECURITY"   score={summary?.pillar3_score ?? null} color="rgba(0,200,83,0.22)" />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
          <span
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.65rem',
              fontWeight: 700,
              letterSpacing: '0.12em',
              opacity: 0.5,
              marginBottom: '0.1rem',
            }}
          >
            OVERALL
          </span>
          <span
            style={{
              fontFamily: 'var(--font-sans)',
              fontSize: '6rem',
              fontWeight: 900,
              lineHeight: 1,
              color: overall !== null ? 'var(--fg)' : 'rgba(10,10,10,0.25)',
              letterSpacing: '-0.04em',
            }}
          >
            {overall !== null ? `${Math.round(overall * 100)}%` : 'NOT RANKED'}
          </span>
        </div>
      </div>
    </div>
  );
}
