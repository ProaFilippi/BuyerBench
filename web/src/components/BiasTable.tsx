import ScoreBar from './ScoreBar';
import type { BiasSusceptibilityRow } from '@/types/report';

interface BiasTableProps {
  rows: BiasSusceptibilityRow[];
}

function bsiColor(bsi: number): string {
  if (bsi <= 0.2) return 'var(--accent3)';
  if (bsi <= 0.5) return 'var(--accent2)';
  return 'var(--accent)';
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

export default function BiasTable({ rows }: BiasTableProps) {
  if (rows.length === 0) {
    return (
      <div className="brutal-box" style={{ padding: '1.5rem', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
        NO BIAS DATA — AGENT NOT TESTED ON PILLAR 2
      </div>
    );
  }

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
            <th style={thStyle}>BIAS TYPE</th>
            <th style={{ ...thStyle, minWidth: '200px' }}>BSI</th>
            <th style={thStyle}>DECISION CHANGED</th>
            <th style={thStyle}>PAIR ID</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={`${row.pair_id}-${row.bias_type}`}
              style={{ background: idx % 2 === 0 ? 'var(--bg)' : '#ece7d8' }}
            >
              <td style={tdStyle}>{row.bias_type}</td>
              <td style={{ ...tdStyle, minWidth: '200px' }}>
                <ScoreBar score={row.bsi} color={bsiColor(row.bsi)} />
              </td>
              <td style={tdStyle}>
                {row.decision_changed ? (
                  <span style={{ color: 'var(--accent)', fontWeight: 700 }}>&#x2717; CHANGED</span>
                ) : (
                  <span style={{ color: 'var(--accent3)', fontWeight: 700 }}>&#x2713; STABLE</span>
                )}
              </td>
              <td style={{ ...tdStyle, opacity: 0.6 }}>{row.pair_id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
