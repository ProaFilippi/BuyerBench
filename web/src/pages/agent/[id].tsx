import Link from 'next/link';
import type { GetStaticPaths, GetStaticProps, InferGetStaticPropsType } from 'next';
import Layout from '@/components/Layout';
import AgentHeader from '@/components/AgentHeader';
import BiasTable from '@/components/BiasTable';
import SecurityTable from '@/components/SecurityTable';
import DeltaTable from '@/components/DeltaTable';
import {
  loadReport,
  computeAgentSummaries,
  getAllAgentIds,
  getBiasRowsForAgent,
  getSecurityRowsForAgent,
  getDeltaRowsForAgent,
} from '@/lib/loadReport';
import type {
  AgentSummary,
  BiasSusceptibilityRow,
  SecurityViolationRow,
  SkillsDeltaRow,
} from '@/types/report';

interface Props {
  agentId: string;
  summary: AgentSummary | null;
  biasRows: BiasSusceptibilityRow[];
  securityRows: SecurityViolationRow[];
  deltaRows: SkillsDeltaRow[];
  generatedAt: string;
}

export const getStaticPaths: GetStaticPaths = async () => {
  const report = loadReport();
  const ids = getAllAgentIds(report);
  return {
    paths: ids.map((id) => ({ params: { id } })),
    fallback: false,
  };
};

export const getStaticProps: GetStaticProps<Props> = async ({ params }) => {
  const agentId = params?.id as string;
  const report = loadReport();
  const summaries = computeAgentSummaries(report);

  return {
    props: {
      agentId,
      summary: summaries.find((s) => s.agent_id === agentId) ?? null,
      biasRows: getBiasRowsForAgent(report, agentId),
      securityRows: getSecurityRowsForAgent(report, agentId),
      deltaRows: getDeltaRowsForAgent(report, agentId),
      generatedAt: report.generated_at,
    },
  };
};

const sectionStyle: React.CSSProperties = {
  marginBottom: '2.5rem',
};

const sectionTitleStyle: React.CSSProperties = {
  fontFamily: 'var(--font-mono)',
  fontSize: '0.75rem',
  fontWeight: 700,
  letterSpacing: '0.12em',
  textTransform: 'uppercase',
  marginBottom: '0.4rem',
};

const explainerStyle: React.CSSProperties = {
  fontFamily: 'var(--font-mono)',
  fontSize: '0.75rem',
  opacity: 0.6,
  marginBottom: '1rem',
  lineHeight: 1.5,
};

const separatorStyle: React.CSSProperties = {
  borderTop: '2px solid var(--fg)',
  marginBottom: '1rem',
};

const backButtonStyle: React.CSSProperties = {
  display: 'inline-block',
  fontFamily: 'var(--font-mono)',
  fontSize: '0.72rem',
  fontWeight: 700,
  letterSpacing: '0.1em',
  color: 'var(--fg)',
  textDecoration: 'none',
  border: '2px solid var(--fg)',
  padding: '0.3rem 0.8rem',
  marginBottom: '2rem',
  boxShadow: '2px 2px 0 var(--fg)',
};

export default function AgentPage({
  agentId,
  summary,
  biasRows,
  securityRows,
  deltaRows,
  generatedAt,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  return (
    <Layout generatedAt={generatedAt}>
      <div style={{ paddingTop: '2rem' }}>
        <Link href="/" style={backButtonStyle}>
          &larr; BACK TO RANKINGS
        </Link>

        <AgentHeader agentId={agentId} summary={summary ?? undefined} />


        {/* Bias Section */}
        <section style={sectionStyle}>
          <div className="brutal-box" style={{ padding: '1.5rem' }}>
            <p style={sectionTitleStyle}>BEHAVIORAL BIAS RESISTANCE</p>
            <div style={separatorStyle} />
            <p style={explainerStyle}>
              BSI measures how often framing changes the agent&apos;s decision. 0.0 = fully rational, 1.0 = fully manipulable.
            </p>
            <BiasTable rows={biasRows} />
          </div>
        </section>

        {/* Security Section */}
        <section style={sectionStyle}>
          <div className="brutal-box" style={{ padding: '1.5rem' }}>
            <p style={sectionTitleStyle}>SECURITY &amp; COMPLIANCE</p>
            <div style={separatorStyle} />
            <p style={explainerStyle}>
              Compliance adherence rate and security violation frequency across Pillar 3 scenarios.
            </p>
            <SecurityTable rows={securityRows} />
          </div>
        </section>

        {/* Delta Section */}
        <section style={sectionStyle}>
          <div className="brutal-box" style={{ padding: '1.5rem' }}>
            <p style={sectionTitleStyle}>TOOL AUGMENTATION DELTA</p>
            <div style={separatorStyle} />
            <p style={explainerStyle}>
              Score change when adding Skills or MCP server vs. baseline prompt-only mode.
            </p>
            <DeltaTable rows={deltaRows} />
          </div>
        </section>
      </div>
    </Layout>
  );
}
