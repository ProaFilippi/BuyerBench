import ScoreBar from './ScoreBar';
import type { SecurityViolationRow } from '@/types/report';

interface SecurityTableProps {
  rows: SecurityViolationRow[];
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

export default function SecurityTable({ rows }: SecurityTableProps) {
  if (rows.length === 0) {
    return (
      <div className="brutal-box" style={{ padding: '1.5rem', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}>
        NO SECURITY DATA — AGENT NOT TESTED ON PILLAR 3
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
            <th style={thStyle}>SCENARIO</th>
            <th style={{ ...thStyle, minWidth: '180px' }}>COMPLIANCE RATE</th>
            <th style={{ ...thStyle, minWidth: '200px' }}>
              VIOLATION FREQ
              <span style={{ display: 'block', fontSize: '0.65rem', fontWeight: 400, opacity: 0.75, letterSpacing: '0.04em' }}>
                LOWER = BETTER
              </span>
            </th>
            <th style={{ ...thStyle, minWidth: '180px' }}>SCORE</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr
              key={row.scenario_id}
              style={{ background: idx % 2 === 0 ? 'var(--bg)' : '#ece7d8' }}
            >
              <td style={tdStyle}>{row.scenario_id}</td>
              <td style={{ ...tdStyle, minWidth: '180px' }}>
                <ScoreBar score={row.compliance_adherence_rate} color="var(--accent3)" />
              </td>
              <td style={{ ...tdStyle, minWidth: '200px' }}>
                {/* Red bar: higher frequency = more red = more violations = worse */}
                <ScoreBar score={row.security_violation_frequency} color="var(--accent)" />
              </td>
              <td style={{ ...tdStyle, minWidth: '180px' }}>
                <ScoreBar score={row.score} color="var(--accent3)" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
