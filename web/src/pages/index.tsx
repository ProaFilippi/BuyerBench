import type { GetStaticProps, InferGetStaticPropsType } from 'next';
import Layout from '@/components/Layout';
import { loadReport, computeAgentSummaries } from '@/lib/loadReport';
import type { AgentSummary, FullReport } from '@/types/report';
import styles from './index.module.css';

interface Props {
  summaries: AgentSummary[];
  generatedAt: string;
  isSampleData: boolean;
  agentCount: number;
  scenarioCount: number;
}

export const getStaticProps: GetStaticProps<Props> = async () => {
  const report: FullReport = loadReport();
  const summaries = computeAgentSummaries(report);
  const isSampleData = report.generated_at === 'SAMPLE DATA';
  const scenarioCount = report.per_pillar_aggregate.reduce((sum, r) => sum + r.n_scenarios, 0);

  return {
    props: {
      summaries,
      generatedAt: report.generated_at,
      isSampleData,
      agentCount: summaries.length,
      scenarioCount,
    },
  };
};

function ScoreBar({ score, color }: { score: number | null; color: string }) {
  if (score === null) {
    return <div className={styles.scoreBarWrap}><span className={styles.naLabel}>N/A</span></div>;
  }
  return (
    <div className={`${styles.scoreBarWrap} brutal-border`}>
      <div
        className={styles.scoreBarFill}
        style={{ width: `${Math.round(score * 100)}%`, background: color }}
      />
      <span className={styles.scoreLabel}>{(score * 100).toFixed(0)}%</span>
    </div>
  );
}

export default function HomePage({ summaries, generatedAt, isSampleData, agentCount, scenarioCount }: InferGetStaticPropsType<typeof getStaticProps>) {
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

      {/* Rankings Table */}
      <section className={styles.tableSection}>
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
                  <td className={styles.agentId}>{agent.agent_id}</td>
                  <td><ScoreBar score={agent.pillar1_score} color="var(--accent)" /></td>
                  <td><ScoreBar score={agent.pillar2_score} color="var(--accent2)" /></td>
                  <td><ScoreBar score={agent.pillar3_score} color="#00c853" /></td>
                  <td><ScoreBar score={agent.overall_score} color="var(--fg)" /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Stat Cards */}
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
