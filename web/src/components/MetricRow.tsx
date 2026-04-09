import ScoreBar from './ScoreBar';
import type { MetricRow as MetricRowData } from '@/types/report';

interface MetricRowProps {
  metric: MetricRowData;
}

export default function MetricRow({ metric }: MetricRowProps) {
  const label = metric.metric.toLowerCase().replace(/_/g, ' ');
  return (
    <tr>
      <td
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.75rem',
          padding: '0.3rem 0.6rem',
          whiteSpace: 'nowrap',
          opacity: 0.8,
        }}
      >
        {label}
      </td>
      <td style={{ padding: '0.3rem 0.6rem', minWidth: '140px' }}>
        <ScoreBar score={metric.mean} color="#666" />
      </td>
      <td
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.72rem',
          padding: '0.3rem 0.6rem',
          whiteSpace: 'nowrap',
          opacity: 0.6,
        }}
      >
        {Math.round(metric.min * 100)}%–{Math.round(metric.max * 100)}%
      </td>
    </tr>
  );
}
