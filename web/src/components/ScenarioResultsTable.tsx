'use client';
import { useState } from 'react';
import ScoreBar from './ScoreBar';
import type { ScenarioResult } from '@/types/report';

interface Props {
  rows: ScenarioResult[];
}

const PILLAR_COLORS: Record<string, string> = {
  PILLAR1: 'var(--accent)',
  PILLAR2: '#e6c700',
  PILLAR3: 'var(--accent3)',
};

function formatScenarioId(id: string): string {
  return id
    .replace(/^p\d+-\d+-/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatAge(timestamp: string | null): string | null {
  if (!timestamp) return null;
  const then = new Date(timestamp).getTime();
  const now = Date.now();
  const diffMs = now - then;
  if (diffMs < 0) return null;
  const mins = Math.floor(diffMs / 60_000);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;
  const weeks = Math.floor(days / 7);
  if (weeks < 5) return `${weeks}w ago`;
  const months = Math.floor(days / 30);
  return `${months}mo ago`;
}

function ageBadgeColor(timestamp: string | null): string {
  if (!timestamp) return 'rgba(0,0,0,0.3)';
  const days = (Date.now() - new Date(timestamp).getTime()) / 86_400_000;
  if (days < 1) return '#16a34a';   // green — fresh
  if (days < 7) return '#ca8a04';   // amber — this week
  return '#dc2626';                  // red — stale
}

export default function ScenarioResultsTable({ rows }: Props) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showErrors, setShowErrors] = useState(false);

  const validRows = rows.filter((r) => !r.is_error);
  const errorCount = rows.length - validRows.length;
  const displayRows = showErrors ? rows : validRows;

  if (rows.length === 0) {
    return (
      <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', opacity: 0.5 }}>
        NO SCENARIO DETAIL DATA
      </p>
    );
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
    fontSize: '0.8rem',
  };

  return (
    <div style={{ overflowX: 'auto' }}>
      {errorCount > 0 && (
        <div style={{
          fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
          marginBottom: '0.6rem', display: 'flex', alignItems: 'center', gap: '0.5rem',
        }}>
          <span style={{ color: '#dc2626', fontWeight: 700 }}>
            {errorCount} ERROR RESULT{errorCount > 1 ? 'S' : ''} HIDDEN
          </span>
          <button
            onClick={() => setShowErrors(!showErrors)}
            style={{
              fontFamily: 'var(--font-mono)', fontSize: '0.68rem', fontWeight: 600,
              background: 'none', border: '1.5px solid var(--fg)', padding: '0.15rem 0.5rem',
              cursor: 'pointer', letterSpacing: '0.06em',
            }}
          >
            {showErrors ? 'HIDE ERRORS' : 'SHOW ERRORS'}
          </button>
        </div>
      )}
      <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '0 2px', fontSize: '0.85rem', tableLayout: 'fixed' }}>
        <colgroup>
          <col style={{ width: '30%' }} />
          <col style={{ width: '10%' }} />
          <col style={{ width: '25%' }} />
          <col style={{ width: '12%' }} />
          <col style={{ width: '12%' }} />
          <col style={{ width: '11%' }} />
        </colgroup>
        <thead>
          <tr>
            <th style={thStyle}>SCENARIO</th>
            <th style={thStyle}>PILLAR</th>
            <th style={thStyle}>SCORE</th>
            <th style={{ ...thStyle, textAlign: 'center' }}>STATUS</th>
            <th style={{ ...thStyle, textAlign: 'center' }}>AGE</th>
            <th style={{ ...thStyle, textAlign: 'center' }}>DETAILS</th>
          </tr>
        </thead>
        <tbody>
          {displayRows.map((row, idx) => {
            const key = `${row.scenario_id}-${row.pillar}`;
            const isExpanded = expandedId === key;
            const color = PILLAR_COLORS[row.pillar] ?? 'var(--fg)';

            return (
              <>
                <tr
                  key={key}
                  style={{
                    background: row.is_error ? '#fef2f2' : (idx % 2 === 0 ? 'var(--bg)' : '#ece7d8'),
                    opacity: row.is_error ? 0.6 : 1,
                    cursor: 'pointer',
                  }}
                  onClick={() => setExpandedId(isExpanded ? null : key)}
                >
                  <td style={{ ...tdStyle, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {formatScenarioId(row.scenario_id)}
                  </td>
                  <td style={tdStyle}>
                    <span style={{
                      background: color,
                      color: '#fff',
                      padding: '0.15rem 0.4rem',
                      fontSize: '0.65rem',
                      fontWeight: 700,
                      letterSpacing: '0.05em',
                    }}>
                      {row.pillar.replace('PILLAR', 'P')}
                    </span>
                  </td>
                  <td style={tdStyle}>
                    <ScoreBar score={row.score} color={color} />
                  </td>
                  <td style={{ ...tdStyle, textAlign: 'center' }}>
                    {row.is_error ? (
                      <span style={{
                        fontWeight: 700, color: '#9333ea', fontSize: '0.7rem',
                        background: '#f3e8ff', padding: '0.1rem 0.35rem',
                        border: '1px solid #9333ea',
                      }}>
                        ERROR
                      </span>
                    ) : (
                      <span style={{
                        fontWeight: 700,
                        color: row.overall_pass ? '#16a34a' : '#dc2626',
                        fontSize: '0.75rem',
                      }}>
                        {row.overall_pass ? 'PASS' : 'FAIL'}
                      </span>
                    )}
                  </td>
                  <td style={{ ...tdStyle, textAlign: 'center' }}>
                    {row.timestamp && (
                      <span style={{
                        fontFamily: 'var(--font-mono)', fontSize: '0.62rem', fontWeight: 600,
                        color: ageBadgeColor(row.timestamp),
                        background: `${ageBadgeColor(row.timestamp)}12`,
                        padding: '0.1rem 0.35rem',
                        border: `1px solid ${ageBadgeColor(row.timestamp)}40`,
                        whiteSpace: 'nowrap',
                      }}>
                        {formatAge(row.timestamp)}
                      </span>
                    )}
                  </td>
                  <td style={{ ...tdStyle, textAlign: 'center', fontSize: '0.7rem', opacity: 0.6 }}>
                    {isExpanded ? '[ - ]' : '[ + ]'}
                  </td>
                </tr>

                {isExpanded && (
                  <tr key={`${key}-detail`} style={{ background: '#f0ebd8' }}>
                    <td colSpan={6} style={{ padding: '1rem 1.5rem' }}>
                      {/* Violations */}
                      {row.violations.length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <p style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.7rem',
                            fontWeight: 700, letterSpacing: '0.08em', marginBottom: '0.3rem',
                          }}>
                            VIOLATIONS
                          </p>
                          <ul style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.75rem',
                            margin: 0, paddingLeft: '1.2rem', lineHeight: 1.6,
                            color: '#dc2626',
                          }}>
                            {row.violations.map((v, i) => <li key={i}>{v}</li>)}
                          </ul>
                        </div>
                      )}

                      {/* Metrics */}
                      {Object.keys(row.metrics).length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <p style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.7rem',
                            fontWeight: 700, letterSpacing: '0.08em', marginBottom: '0.3rem',
                          }}>
                            METRICS
                          </p>
                          <div style={{
                            display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
                            gap: '0.3rem',
                          }}>
                            {Object.entries(row.metrics).map(([k, v]) => (
                              <div key={k} style={{
                                fontFamily: 'var(--font-mono)', fontSize: '0.75rem',
                                display: 'flex', justifyContent: 'space-between',
                                padding: '0.2rem 0.5rem', background: 'rgba(0,0,0,0.04)',
                              }}>
                                <span style={{ opacity: 0.7 }}>{k.replace(/_/g, ' ')}</span>
                                <span style={{ fontWeight: 600 }}>{typeof v === 'number' ? v.toFixed(2) : String(v)}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Decisions */}
                      {row.decisions && Object.keys(row.decisions).length > 0 && (
                        <div style={{ marginBottom: '1rem' }}>
                          <p style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.7rem',
                            fontWeight: 700, letterSpacing: '0.08em', marginBottom: '0.3rem',
                          }}>
                            AGENT DECISIONS
                          </p>
                          <pre style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
                            background: '#1a1a1a', color: '#e2e2e2',
                            padding: '0.8rem', overflowX: 'auto',
                            maxHeight: '300px', lineHeight: 1.5,
                            border: '2px solid var(--fg)',
                            whiteSpace: 'pre-wrap', wordBreak: 'break-word',
                          }}>
                            {JSON.stringify(row.decisions, null, 2)}
                          </pre>
                        </div>
                      )}

                      {/* Raw Output */}
                      {row.raw_output && (
                        <div>
                          <p style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.7rem',
                            fontWeight: 700, letterSpacing: '0.08em', marginBottom: '0.3rem',
                          }}>
                            RAW LLM OUTPUT
                          </p>
                          <pre style={{
                            fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
                            background: '#1a1a1a', color: '#a3e635',
                            padding: '0.8rem', overflowX: 'auto',
                            maxHeight: '400px', lineHeight: 1.5,
                            border: '2px solid var(--fg)',
                            whiteSpace: 'pre-wrap', wordBreak: 'break-word',
                          }}>
                            {row.raw_output}
                          </pre>
                        </div>
                      )}

                      {/* Notes */}
                      {row.notes && (
                        <p style={{
                          fontFamily: 'var(--font-mono)', fontSize: '0.72rem',
                          opacity: 0.6, marginTop: '0.5rem',
                        }}>
                          {row.notes}
                        </p>
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
