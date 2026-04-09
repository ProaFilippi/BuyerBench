import ScoreBar from './ScoreBar';
import type { SkillsDeltaRow } from '@/types/report';

interface DeltaTableProps {
  rows: SkillsDeltaRow[];
}

const thStyle: React.CSSProperties = {
  background: 'var(--fg)',
  color: 'var(--bg)',
  padding: '0.6rem 0.8rem',
  textAlign: 'left',
  fontFamily: 'var(--font-mono)',
  fontSize: '0.75rem',
  letterSpacing: '0.08em',
  fontWeight: 600,
  whiteSpace: 'nowrap',
};

const tdStyle: React.CSSProperties = {
  padding: '0.55rem 0.8rem',
  borderBottom: '1px solid rgba(10,10,10,0.15)',
  verticalAlign: 'middle',
  fontFamily: 'var(--font-mono)',
  fontSize: '0.82rem',
};

const sectionHeaderStyle: React.CSSProperties = {
  padding: '0.5rem 0.8rem',
  fontFamily: 'var(--font-mono)',
  fontSize: '0.72rem',
  fontWeight: 700,
  letterSpacing: '0.12em',
  background: 'rgba(10,10,10,0.08)',
  borderBottom: '2px solid var(--fg)',
};

export default function DeltaTable({ rows }: DeltaTableProps) {
  if (rows.length === 0) {
    return (
      <div className="brutal-box" style={{ padding: '1.5rem', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
        NO DELTA DATA — THIS IS A BASELINE AGENT
      </div>
    );
  }

  const pillars = Array.from(new Set(rows.map((r) => r.pillar))).sort();

  return (
    <div style={{ overflowX: 'auto' }}>
      <table
        style={{
          width: '100%',
          borderCollapse: 'separate',
          borderSpacing: '0 2px',
          fontSize: '0.85rem',
        }}
      >
        <thead>
          <tr>
            <th style={thStyle}>PILLAR</th>
            <th style={thStyle}>MODE</th>
            <th style={{ ...thStyle, minWidth: '160px' }}>BASELINE</th>
            <th style={{ ...thStyle, minWidth: '160px' }}>WITH TOOLS</th>
            <th style={thStyle}>DELTA</th>
          </tr>
        </thead>
        <tbody>
          {pillars.map((pillar) => {
            const pillarRows = rows.filter((r) => r.pillar === pillar);
            return (
              <>
                <tr key={`header-${pillar}`}>
                  <td
                    colSpan={5}
                    style={sectionHeaderStyle}
                  >
                    {pillar}
                  </td>
                </tr>
                {pillarRows.map((row, idx) => (
                  <tr
                    key={`${pillar}-${row.mode}`}
                    style={{ background: idx % 2 === 0 ? 'var(--bg)' : '#ece7d8' }}
                  >
                    <td style={{ ...tdStyle, opacity: 0.5 }}>{row.pillar}</td>
                    <td style={tdStyle}>{row.mode.toUpperCase()}</td>
                    <td style={{ ...tdStyle, minWidth: '160px' }}>
                      <ScoreBar score={row.baseline_score} color="rgba(10,10,10,0.35)" />
                    </td>
                    <td style={{ ...tdStyle, minWidth: '160px' }}>
                      <ScoreBar score={row.variant_score} color="rgba(10,10,10,0.35)" />
                    </td>
                    <td style={tdStyle}>
                      {row.delta > 0 ? (
                        <span style={{ color: 'var(--accent3)', fontWeight: 700 }}>
                          +{row.delta.toFixed(2)}
                        </span>
                      ) : row.delta < 0 ? (
                        <span style={{ color: 'var(--accent)', fontWeight: 700 }}>
                          {row.delta.toFixed(2)}
                        </span>
                      ) : (
                        <span style={{ color: 'rgba(10,10,10,0.4)', fontWeight: 700 }}>0.00</span>
                      )}
                    </td>
                  </tr>
                ))}
              </>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
