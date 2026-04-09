'use client';
import { useState } from 'react';
import ScoreBar from './ScoreBar';
import MetricRow from './MetricRow';
import type { PillarAggregate, MetricRow as MetricRowData } from '@/types/report';

interface PillarTableProps {
  rows: PillarAggregate[];
  metrics: Record<string, MetricRowData[]>;
  pillar: string;
  accentColor: string;
}

function formatAgentId(id: string): string {
  if (id.startsWith('openrouter-')) {
    const parts = id.replace('openrouter-', '').split('-');
    // First segment is the provider family — uppercase it
    parts[0] = parts[0].toUpperCase();
    return parts.join(' ');
  }
  return id.replace(/-/g, ' ');
}

export default function PillarTable({ rows, metrics, accentColor }: PillarTableProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  function toggleRow(agentId: string) {
    setExpandedId((prev) => (prev === agentId ? null : agentId));
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
            <th style={{ ...thStyle, width: '56px', textAlign: 'center' }}>RANK</th>
            <th style={thStyle}>AGENT</th>
            <th style={{ ...thStyle, minWidth: '180px' }}>SCORE</th>
            <th style={thStyle}>VARIANCE</th>
            <th style={thStyle}>SCENARIOS</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => {
            const isFirst = idx === 0;
            const isExpanded = expandedId === row.agent_id;
            const agentMetrics = metrics[row.agent_id] ?? [];

            const rowStyle: React.CSSProperties = {
              cursor: 'pointer',
              background: isFirst ? 'var(--accent2)' : idx % 2 === 0 ? 'var(--bg)' : '#ece7d8',
              borderLeft: isFirst ? `6px solid ${accentColor}` : undefined,
            };

            const tdStyle: React.CSSProperties = {
              padding: '0.55rem 0.8rem',
              borderBottom: '1px solid rgba(10,10,10,0.15)',
              verticalAlign: 'middle',
            };

            return (
              <>
                <tr key={row.agent_id} style={rowStyle} onClick={() => toggleRow(row.agent_id)}>
                  <td style={{ ...tdStyle, textAlign: 'center', fontWeight: 700 }}>
                    <span style={{ color: isFirst ? accentColor : 'inherit' }}>#{idx + 1}</span>
                  </td>
                  <td
                    style={{
                      ...tdStyle,
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.8rem',
                      whiteSpace: 'nowrap',
                      minWidth: '200px',
                    }}
                  >
                    {formatAgentId(row.agent_id)}
                  </td>
                  <td style={{ ...tdStyle, minWidth: '180px' }}>
                    <ScoreBar score={row.mean_score} color={accentColor} />
                  </td>
                  <td
                    style={{
                      ...tdStyle,
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.8rem',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    ±{row.std.toFixed(2)}
                  </td>
                  <td style={{ ...tdStyle, fontFamily: 'var(--font-mono)', fontSize: '0.8rem' }}>
                    {row.n_scenarios}
                  </td>
                </tr>
                {isExpanded && (
                  <tr key={`${row.agent_id}-metrics`} style={{ background: '#f0ebd8' }}>
                    <td colSpan={5} style={{ padding: '0.5rem 1.5rem 0.75rem' }}>
                      {agentMetrics.length === 0 ? (
                        <span
                          style={{
                            fontFamily: 'var(--font-mono)',
                            fontSize: '0.75rem',
                            opacity: 0.5,
                          }}
                        >
                          no metric breakdown available
                        </span>
                      ) : (
                        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                          <tbody>
                            {agentMetrics.map((m) => (
                              <MetricRow key={m.metric} metric={m} />
                            ))}
                          </tbody>
                        </table>
                      )}
                    </td>
                  </tr>
                )}
              </>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
