import fs from 'fs';
import path from 'path';
import type { FullReport, AgentSummary } from '@/types/report';

const SAMPLE_REPORT: FullReport = {
  generated_at: 'SAMPLE DATA',
  experiment_dir: 'results/experiments',
  per_pillar_aggregate: [
    { agent_id: 'mock-agent-v1',               pillar: 'PILLAR1', mean_score: 1.00, std: 0.00, min: 1.0, max: 1.0, n_scenarios: 6 },
    { agent_id: 'mock-agent-v1',               pillar: 'PILLAR2', mean_score: 1.00, std: 0.00, min: 1.0, max: 1.0, n_scenarios: 6 },
    { agent_id: 'mock-agent-v1',               pillar: 'PILLAR3', mean_score: 1.00, std: 0.00, min: 1.0, max: 1.0, n_scenarios: 6 },
    { agent_id: 'openrouter-openai-gpt-4o',    pillar: 'PILLAR1', mean_score: 0.70, std: 0.12, min: 0.5, max: 0.9, n_scenarios: 6 },
    { agent_id: 'openrouter-openai-gpt-4o',    pillar: 'PILLAR2', mean_score: 0.60, std: 0.15, min: 0.4, max: 0.8, n_scenarios: 6 },
    { agent_id: 'openrouter-openai-gpt-4o',    pillar: 'PILLAR3', mean_score: 0.80, std: 0.10, min: 0.6, max: 1.0, n_scenarios: 6 },
    { agent_id: 'claude-code-baseline',         pillar: 'PILLAR1', mean_score: 0.60, std: 0.18, min: 0.3, max: 0.9, n_scenarios: 6 },
    { agent_id: 'claude-code-baseline',         pillar: 'PILLAR2', mean_score: 0.50, std: 0.20, min: 0.2, max: 0.8, n_scenarios: 6 },
    { agent_id: 'claude-code-baseline',         pillar: 'PILLAR3', mean_score: 0.70, std: 0.15, min: 0.5, max: 0.9, n_scenarios: 6 },
    { agent_id: 'codex-baseline',               pillar: 'PILLAR1', mean_score: 0.50, std: 0.22, min: 0.2, max: 0.8, n_scenarios: 6 },
    { agent_id: 'codex-baseline',               pillar: 'PILLAR2', mean_score: 0.40, std: 0.18, min: 0.1, max: 0.7, n_scenarios: 6 },
    { agent_id: 'codex-baseline',               pillar: 'PILLAR3', mean_score: 0.60, std: 0.20, min: 0.3, max: 0.9, n_scenarios: 6 },
    { agent_id: 'negmas',                       pillar: 'PILLAR1', mean_score: 0.40, std: 0.25, min: 0.0, max: 0.7, n_scenarios: 6 },
    { agent_id: 'negmas',                       pillar: 'PILLAR2', mean_score: 0.30, std: 0.20, min: 0.0, max: 0.6, n_scenarios: 6 },
    { agent_id: 'negmas',                       pillar: 'PILLAR3', mean_score: 0.20, std: 0.15, min: 0.0, max: 0.5, n_scenarios: 6 },
  ],
  per_metric_breakdown: {},
  bias_susceptibility_table: [],
  security_violation_table: [],
  skills_mcp_delta_table: [],
};

export function loadReport(): FullReport {
  const reportPath = path.join(process.cwd(), '..', 'results', 'experiments', 'FULL-REPORT.json');
  try {
    const raw = fs.readFileSync(reportPath, 'utf-8');
    return JSON.parse(raw) as FullReport;
  } catch {
    return SAMPLE_REPORT;
  }
}

export function computeAgentSummaries(report: FullReport): AgentSummary[] {
  const byAgent = new Map<string, { p1: number | null; p2: number | null; p3: number | null; n: number }>();

  for (const row of report.per_pillar_aggregate) {
    if (!byAgent.has(row.agent_id)) {
      byAgent.set(row.agent_id, { p1: null, p2: null, p3: null, n: 0 });
    }
    const entry = byAgent.get(row.agent_id)!;
    if (row.pillar === 'PILLAR1') entry.p1 = row.mean_score;
    else if (row.pillar === 'PILLAR2') entry.p2 = row.mean_score;
    else if (row.pillar === 'PILLAR3') entry.p3 = row.mean_score;
    entry.n += row.n_scenarios;
  }

  const summaries: AgentSummary[] = [];
  for (const [agent_id, { p1, p2, p3, n }] of byAgent) {
    const scores = [p1, p2, p3].filter((s): s is number => s !== null);
    const overall_score = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    summaries.push({ agent_id, pillar1_score: p1, pillar2_score: p2, pillar3_score: p3, overall_score, n_scenarios_total: n });
  }

  return summaries.sort((a, b) => b.overall_score - a.overall_score);
}
