import { useState } from 'react';
import Link from 'next/link';
import type { GetStaticProps, InferGetStaticPropsType } from 'next';
import Layout from '@/components/Layout';
import ScoreBar from '@/components/ScoreBar';
import PillarTabs from '@/components/PillarTabs';
import PillarTable from '@/components/PillarTable';
import {
  loadReport,
  computeAgentSummaries,
  computePillarLeaderboard,
  getMetricsForAgent,
} from '@/lib/loadReport';
import type { AgentSummary, PillarAggregate, MetricRow } from '@/types/report';
import styles from './index.module.css';

interface Props {
  summaries: AgentSummary[];
  generatedAt: string;
  isSampleData: boolean;
  agentCount: number;
  scenarioCount: number;
  pillar1: PillarAggregate[];
  pillar2: PillarAggregate[];
  pillar3: PillarAggregate[];
  metricsP1: Record<string, MetricRow[]>;
  metricsP2: Record<string, MetricRow[]>;
  metricsP3: Record<string, MetricRow[]>;
}

const TABS = [
  { id: 'OVERALL', label: 'OVERALL' },
  { id: 'PILLAR1', label: 'CAPABILITY' },
  { id: 'PILLAR2', label: 'ECONOMICS' },
  { id: 'PILLAR3', label: 'SECURITY' },
];

function formatAgentId(id: string): string {
  if (id.startsWith('openrouter-')) {
    const parts = id.replace('openrouter-', '').split('-');
    parts[0] = parts[0].toUpperCase();
    return parts.join(' ');
  }
  return id.replace(/-/g, ' ');
}

const PILLAR_COLORS: Record<string, string> = {
  PILLAR1: 'var(--accent)',
  PILLAR2: '#e6c700',
  PILLAR3: 'var(--accent3)',
};

export const getStaticProps: GetStaticProps<Props> = async () => {
  const report = loadReport();
  const summaries = computeAgentSummaries(report);
  const isSampleData = report.generated_at === 'SAMPLE DATA';
  const scenarioCount = report.per_pillar_aggregate.reduce((sum, r) => sum + r.n_scenarios, 0);

  const pillar1 = computePillarLeaderboard(report, 'PILLAR1');
  const pillar2 = computePillarLeaderboard(report, 'PILLAR2');
  const pillar3 = computePillarLeaderboard(report, 'PILLAR3');

  function buildMetricsMap(rows: PillarAggregate[], pillar: string): Record<string, MetricRow[]> {
    const map: Record<string, MetricRow[]> = {};
    for (const row of rows) {
      map[row.agent_id] = getMetricsForAgent(report, pillar, row.agent_id);
    }
    return map;
  }

  return {
    props: {
      summaries,
      generatedAt: report.generated_at,
      isSampleData,
      agentCount: summaries.length,
      scenarioCount,
      pillar1,
      pillar2,
      pillar3,
      metricsP1: buildMetricsMap(pillar1, 'PILLAR1'),
      metricsP2: buildMetricsMap(pillar2, 'PILLAR2'),
      metricsP3: buildMetricsMap(pillar3, 'PILLAR3'),
    },
  };
};

export default function HomePage({
  summaries,
  generatedAt,
  isSampleData,
  agentCount,
  scenarioCount,
  pillar1,
  pillar2,
  pillar3,
  metricsP1,
  metricsP2,
  metricsP3,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  const [activeTab, setActiveTab] = useState('OVERALL');

  return (
    <Layout generatedAt={generatedAt}>
      {/* Hero */}
      <section className={styles.hero}>
        <h1 className={styles.headline}>AI BUYER AGENT<br />RANKINGS</h1>
        <p className={styles.subtitle}>
          Pillar 1: Capability&nbsp;·&nbsp;Pillar 2: Economics&nbsp;·&nbsp;Pillar 3: Security
        </p>
        {isSampleData
          ? <span className="tag">SAMPLE DATA</span>
          : <span className="tag tag-accent">LIVE DATA</span>
        }
      </section>

      {/* Leaderboard with pillar tabs */}
      <section className={styles.tableSection}>
        <PillarTabs activeTab={activeTab} onChange={setActiveTab} tabs={TABS} />

        {activeTab === 'OVERALL' && (
          <div className={`${styles.tableWrap} brutal-border`}>
            <table className={styles.table}>
              <thead>
                <tr className={styles.thead}>
                  <th>RANK</th>
                  <th>AGENT</th>
                  <th>CAPABILITY (P1)</th>
                  <th>ECONOMICS (P2)</th>
                  <th>SECURITY (P3)</th>
                  <th>OVERALL</th>
                </tr>
              </thead>
              <tbody>
                {summaries.map((agent, idx) => (
                  <tr
                    key={agent.agent_id}
                    className={styles.row}
                    style={{
                      background: idx % 2 === 0 ? 'var(--bg)' : '#ece7d8',
                      borderLeft: idx === 0 ? '6px solid var(--accent)' : undefined,
                    }}
                  >
                    <td className={styles.rank}>
                      <span className={idx === 0 ? styles.rankFirst : styles.rankNum}>
                        #{idx + 1}
                      </span>
                    </td>
                    <td className={styles.agentId}>
                      <Link
                        href={`/agent/${agent.agent_id}`}
                        style={{ color: 'var(--fg)', textDecoration: 'underline', textDecorationStyle: 'wavy' }}
                      >
                        {formatAgentId(agent.agent_id)}
                      </Link>
                    </td>
                    <td>
                      {agent.pillar1_score !== null
                        ? <ScoreBar score={agent.pillar1_score} color="var(--accent)" />
                        : <span className={styles.naLabel}>N/A</span>}
                    </td>
                    <td>
                      {agent.pillar2_score !== null
                        ? <ScoreBar score={agent.pillar2_score} color="#e6c700" />
                        : <span className={styles.naLabel}>N/A</span>}
                    </td>
                    <td>
                      {agent.pillar3_score !== null
                        ? <ScoreBar score={agent.pillar3_score} color="var(--accent3)" />
                        : <span className={styles.naLabel}>N/A</span>}
                    </td>
                    <td>
                      <ScoreBar score={agent.overall_score} color="var(--fg)" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'PILLAR1' && (
          <div className="brutal-border">
            <PillarTable
              rows={pillar1}
              metrics={metricsP1}
              pillar="PILLAR1"
              accentColor={PILLAR_COLORS.PILLAR1}
            />
          </div>
        )}

        {activeTab === 'PILLAR2' && (
          <div className="brutal-border">
            <PillarTable
              rows={pillar2}
              metrics={metricsP2}
              pillar="PILLAR2"
              accentColor={PILLAR_COLORS.PILLAR2}
            />
          </div>
        )}

        {activeTab === 'PILLAR3' && (
          <div className="brutal-border">
            <PillarTable
              rows={pillar3}
              metrics={metricsP3}
              pillar="PILLAR3"
              accentColor={PILLAR_COLORS.PILLAR3}
            />
          </div>
        )}
      </section>

      {/* Stat strip + cards */}
      <section className={styles.statsRow}>
        <div className={`${styles.statCard} brutal-box`}>
          <span className={styles.statNum}>{agentCount}</span>
          <span className={styles.statLabel}>AGENTS EVALUATED</span>
        </div>
        <div className={`${styles.statCard} brutal-box`}>
          <span className={styles.statNum}>{scenarioCount}</span>
          <span className={styles.statLabel}>SCENARIOS TESTED</span>
        </div>
        <div className={`${styles.statCard} brutal-box`}>
          <span className={styles.statNum}>3</span>
          <span className={styles.statLabel}>PILLARS</span>
        </div>
      </section>
    </Layout>
  );
}
