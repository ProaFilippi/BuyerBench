import type { GetStaticProps, InferGetStaticPropsType } from 'next';
import Link from 'next/link';
import Layout from '@/components/Layout';
import ScenarioCount from '@/components/ScenarioCount';
import { loadReport } from '@/lib/loadReport';
import type { PillarAggregate } from '@/types/report';
import styles from './about.module.css';

interface Props {
  pillarAggregates: PillarAggregate[];
  generatedAt: string;
}

export const getStaticProps: GetStaticProps<Props> = async () => {
  const report = loadReport();
  return {
    props: {
      pillarAggregates: report.per_pillar_aggregate,
      generatedAt: report.generated_at,
    },
  };
};

export default function AboutPage({ pillarAggregates, generatedAt }: InferGetStaticPropsType<typeof getStaticProps>) {
  return (
    <Layout generatedAt={generatedAt} title="About — BuyerBench">
      <div className={styles.page}>
        <div className={styles.backLink}>
          <Link href="/" className={styles.back}>← BACK TO RANKINGS</Link>
        </div>

        <h1 className={styles.headline}>ABOUT BUYERBENCH</h1>

        <div className={styles.section}>
          <ScenarioCount pillarAggregates={pillarAggregates} />
        </div>

        {/* Section 1 */}
        <section className={styles.section}>
          <div className={styles.accentBox}>
            <h2 className={styles.sectionTitle}>WHAT IS BUYERBENCH</h2>
            <p className={styles.body}>
              BuyerBench is an open-source benchmark framework for evaluating AI buyer agents
              across three dimensions of real-world procurement performance. The framework runs
              agents through structured scenarios and scores them on three pillars:{' '}
              <strong>Agent Intelligence &amp; Operational Capability</strong> (can the agent
              execute buyer workflows?),{' '}
              <strong>Economic Decision Quality &amp; Behavioral Robustness</strong> (does the
              agent make rational decisions and resist cognitive biases?), and{' '}
              <strong>Security, Compliance &amp; Market Readiness</strong> (does the agent
              follow payment security practices and detect fraud?). Each pillar is scored
              independently, producing a multi-dimensional evaluation profile rather than a
              single collapsed number.
            </p>
          </div>
        </section>

        {/* Section 2 */}
        <section className={styles.section}>
          <div className={styles.accentBox}>
            <h2 className={styles.sectionTitle}>PILLAR 1 — CAPABILITY</h2>
            <p className={styles.body} style={{ marginBottom: '1rem' }}>
              Measures whether the agent can execute core buyer workflows end-to-end. Key metrics:
            </p>
            <ul className={styles.list}>
              <li><span className={styles.bullet}>▸</span> <strong>Task completion rate</strong> — did the agent successfully finish the scenario objective?</li>
              <li><span className={styles.bullet}>▸</span> <strong>Supplier match accuracy</strong> — did the agent select the correct supplier given the constraints?</li>
              <li><span className={styles.bullet}>▸</span> <strong>Tool usage efficiency</strong> — did the agent invoke the right tools in the right order without unnecessary calls?</li>
              <li><span className={styles.bullet}>▸</span> <strong>Quote comparison correctness</strong> — did the agent correctly parse and compare multi-vendor quotes?</li>
              <li><span className={styles.bullet}>▸</span> <strong>Multi-step workflow accuracy</strong> — did the agent maintain context across sequential procurement steps?</li>
            </ul>
          </div>
        </section>

        {/* Section 3 */}
        <section className={styles.section}>
          <div className={styles.accentBox}>
            <h2 className={styles.sectionTitle}>PILLAR 2 — BEHAVIORAL ECONOMICS</h2>
            <p className={styles.body} style={{ marginBottom: '1rem' }}>
              Tests whether agents make economically rational decisions when presentation is
              manipulated. Scenarios come in controlled <strong>variant pairs</strong> where the
              underlying economics are identical but framing differs:
            </p>
            <ul className={styles.list}>
              <li><span className={styles.bullet}>▸</span> <strong>BASELINE</strong> — neutral presentation with no manipulation</li>
              <li><span className={styles.bullet}>▸</span> <strong>ANCHOR_HIGH</strong> — an artificially high price anchor is introduced before the real options</li>
              <li><span className={styles.bullet}>▸</span> <strong>FRAMING_GAIN / FRAMING_LOSS</strong> — identical outcomes framed as gains vs. losses</li>
              <li><span className={styles.bullet}>▸</span> <strong>DECOY</strong> — an asymmetrically dominated option is added to nudge choice</li>
              <li><span className={styles.bullet}>▸</span> <strong>SCARCITY</strong> — artificial urgency or low-stock cues are injected</li>
              <li><span className={styles.bullet}>▸</span> <strong>SUNK_COST</strong> — prior irrelevant expenditures are mentioned to trigger sunk cost fallacy</li>
            </ul>
            <p className={styles.body} style={{ marginTop: '1rem' }}>
              The <strong>Bias Susceptibility Index (BSI)</strong> measures how much an
              agent&apos;s decision changes between the BASELINE and manipulated variants.
              BSI = 0 means perfect resistance; BSI = 1 means the agent was fully manipulated.
              Scores below 0.2 are considered robust; above 0.5 indicates significant susceptibility.
            </p>
          </div>
        </section>

        {/* Section 4 */}
        <section className={styles.section}>
          <div className={styles.accentBox}>
            <h2 className={styles.sectionTitle}>PILLAR 3 — SECURITY &amp; COMPLIANCE</h2>
            <p className={styles.body} style={{ marginBottom: '1rem' }}>
              Evaluates whether agents enforce payment security practices and detect compliance
              violations. Test categories:
            </p>
            <ul className={styles.list}>
              <li><span className={styles.bullet}>▸</span> <strong>Fraud detection</strong> — identifying and rejecting suspicious transactions, duplicate invoices, and social engineering attempts</li>
              <li><span className={styles.bullet}>▸</span> <strong>Credential protection</strong> — correct treatment of API keys, payment tokens, and financial credentials (never logged, never echoed)</li>
              <li><span className={styles.bullet}>▸</span> <strong>Prompt injection resistance</strong> — ignoring adversarial instructions embedded in supplier data or invoices</li>
              <li><span className={styles.bullet}>▸</span> <strong>Authorization enforcement</strong> — respecting vendor approval lists and permission boundaries</li>
              <li><span className={styles.bullet}>▸</span> <strong>Secure transaction sequencing</strong> — correct ordering of authorization, verification, and payment steps</li>
              <li><span className={styles.bullet}>▸</span> <strong>Regulatory compliance</strong> — following operational constraints required by payment networks (PCI-DSS alignment)</li>
            </ul>
          </div>
        </section>

        {/* Section 5 */}
        <section className={styles.section}>
          <div className={styles.accentBox}>
            <h2 className={styles.sectionTitle}>HOW TO RUN</h2>
            <p className={styles.body} style={{ marginBottom: '1rem' }}>
              Install the package, run the benchmark against any configured agent, generate a
              report, then rebuild the site:
            </p>
            <pre className={styles.codeBlock}>{`# 1. Install BuyerBench and dev dependencies
pip install -e ".[dev]"

# 2. Run the benchmark against a named agent (18 scenarios across 3 pillars)
python -m buyerbench run --agent <name>

# 3. Generate FULL-REPORT.json + FULL-REPORT.md from experiment results
python -m buyerbench report --experiment-dir results/experiments

# 4. Rebuild the web dashboard
cd web && npm run build`}</pre>
            <p className={styles.body} style={{ marginTop: '1rem' }}>
              Available agent IDs include <code className={styles.code}>mock-agent-v1</code>,{' '}
              <code className={styles.code}>claude-code-baseline</code>,{' '}
              <code className={styles.code}>codex-baseline</code>,{' '}
              <code className={styles.code}>gemini-baseline</code>, and OpenRouter-hosted models.
              Use <code className={styles.code}>--agent all</code> to run all configured agents sequentially.
            </p>
          </div>
        </section>

        {/* Section 6 */}
        <section className={styles.section}>
          <div className={styles.accentBox}>
            <h2 className={styles.sectionTitle}>DATA FORMAT</h2>
            <p className={styles.body}>
              The benchmark generates a single <code className={styles.code}>FULL-REPORT.json</code>{' '}
              file inside <code className={styles.code}>results/experiments/</code> containing
              per-pillar aggregate scores, per-metric breakdowns, bias susceptibility tables,
              security violation records, and skills/MCP delta tables — all keyed by{' '}
              <code className={styles.code}>agent_id</code>. The web dashboard reads this file
              at build time via <code className={styles.code}>src/lib/loadReport.ts</code> and
              falls back to embedded sample data when no live report is present.
            </p>
          </div>
        </section>
      </div>
    </Layout>
  );
}
