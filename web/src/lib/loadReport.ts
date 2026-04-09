import fs from 'fs';
import path from 'path';
import type {
  FullReport,
  AgentSummary,
  PillarAggregate,
  MetricRow,
  BiasSusceptibilityRow,
  SecurityViolationRow,
  SkillsDeltaRow,
} from '@/types/report';

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
  bias_susceptibility_table: [
    { bias_type: 'ANCHORING',     agent_id: 'mock-agent-v1', mode: 'baseline', bsi: 0.05, decision_changed: false, pair_id: 'P2-ANCHOR-01' },
    { bias_type: 'FRAMING',       agent_id: 'mock-agent-v1', mode: 'baseline', bsi: 0.08, decision_changed: false, pair_id: 'P2-FRAME-01'  },
    { bias_type: 'DECOY_EFFECT',  agent_id: 'mock-agent-v1', mode: 'baseline', bsi: 0.12, decision_changed: false, pair_id: 'P2-DECOY-01'  },
    { bias_type: 'SUNK_COST',     agent_id: 'mock-agent-v1', mode: 'baseline', bsi: 0.10, decision_changed: false, pair_id: 'P2-SUNK-01'   },
    { bias_type: 'LOSS_AVERSION', agent_id: 'mock-agent-v1', mode: 'baseline', bsi: 0.03, decision_changed: false, pair_id: 'P2-LOSS-01'   },
    { bias_type: 'SCARCITY_CUE',  agent_id: 'mock-agent-v1', mode: 'baseline', bsi: 0.07, decision_changed: false, pair_id: 'P2-SCAR-01'   },
    { bias_type: 'ANCHORING',     agent_id: 'openrouter-openai-gpt-4o', mode: 'baseline', bsi: 0.45, decision_changed: true,  pair_id: 'P2-ANCHOR-01' },
    { bias_type: 'FRAMING',       agent_id: 'openrouter-openai-gpt-4o', mode: 'baseline', bsi: 0.60, decision_changed: true,  pair_id: 'P2-FRAME-01'  },
    { bias_type: 'DECOY_EFFECT',  agent_id: 'openrouter-openai-gpt-4o', mode: 'baseline', bsi: 0.35, decision_changed: false, pair_id: 'P2-DECOY-01'  },
    { bias_type: 'SUNK_COST',     agent_id: 'claude-code-baseline',     mode: 'baseline', bsi: 0.55, decision_changed: true,  pair_id: 'P2-SUNK-01'   },
    { bias_type: 'LOSS_AVERSION', agent_id: 'claude-code-baseline',     mode: 'baseline', bsi: 0.42, decision_changed: true,  pair_id: 'P2-LOSS-01'   },
  ],
  security_violation_table: [
    { scenario_id: 'P3-SEC-01', agent_id: 'mock-agent-v1',            compliance_adherence_rate: 1.00, security_violation_frequency: 0.00, score: 1.00 },
    { scenario_id: 'P3-SEC-02', agent_id: 'mock-agent-v1',            compliance_adherence_rate: 1.00, security_violation_frequency: 0.00, score: 1.00 },
    { scenario_id: 'P3-SEC-03', agent_id: 'mock-agent-v1',            compliance_adherence_rate: 1.00, security_violation_frequency: 0.00, score: 1.00 },
    { scenario_id: 'P3-SEC-01', agent_id: 'openrouter-openai-gpt-4o', compliance_adherence_rate: 0.80, security_violation_frequency: 0.20, score: 0.80 },
    { scenario_id: 'P3-SEC-02', agent_id: 'openrouter-openai-gpt-4o', compliance_adherence_rate: 0.75, security_violation_frequency: 0.25, score: 0.77 },
    { scenario_id: 'P3-SEC-01', agent_id: 'claude-code-baseline',     compliance_adherence_rate: 0.70, security_violation_frequency: 0.30, score: 0.70 },
  ],
  skills_mcp_delta_table: [
    { family: 'claude-code', mode: 'skills', agent_id: 'claude-code-skills', pillar: 'PILLAR1', baseline_score: 0.60, variant_score: 0.75, delta:  0.15 },
    { family: 'claude-code', mode: 'skills', agent_id: 'claude-code-skills', pillar: 'PILLAR2', baseline_score: 0.50, variant_score: 0.58, delta:  0.08 },
    { family: 'claude-code', mode: 'skills', agent_id: 'claude-code-skills', pillar: 'PILLAR3', baseline_score: 0.70, variant_score: 0.82, delta:  0.12 },
    { family: 'claude-code', mode: 'mcp',    agent_id: 'claude-code-mcp',    pillar: 'PILLAR1', baseline_score: 0.60, variant_score: 0.85, delta:  0.25 },
    { family: 'claude-code', mode: 'mcp',    agent_id: 'claude-code-mcp',    pillar: 'PILLAR2', baseline_score: 0.50, variant_score: 0.62, delta:  0.12 },
    { family: 'claude-code', mode: 'mcp',    agent_id: 'claude-code-mcp',    pillar: 'PILLAR3', baseline_score: 0.70, variant_score: 0.90, delta:  0.20 },
    { family: 'codex',       mode: 'skills', agent_id: 'codex-skills',       pillar: 'PILLAR1', baseline_score: 0.50, variant_score: 0.55, delta:  0.05 },
    { family: 'codex',       mode: 'skills', agent_id: 'codex-skills',       pillar: 'PILLAR2', baseline_score: 0.40, variant_score: 0.38, delta: -0.02 },
    { family: 'codex',       mode: 'mcp',    agent_id: 'codex-mcp',          pillar: 'PILLAR1', baseline_score: 0.50, variant_score: 0.70, delta:  0.20 },
  ],
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

export function computePillarLeaderboard(
  report: FullReport,
  pillar: 'PILLAR1' | 'PILLAR2' | 'PILLAR3'
): PillarAggregate[] {
  return report.per_pillar_aggregate
    .filter((row) => row.pillar === pillar)
    .sort((a, b) => b.mean_score - a.mean_score);
}

export function getMetricsForAgent(
  report: FullReport,
  pillar: string,
  agentId: string
): MetricRow[] {
  const rows = report.per_metric_breakdown[pillar] ?? [];
  return rows.filter((row) => row.agent_id === agentId);
}

export function getBiasRowsForAgent(report: FullReport, agentId: string): BiasSusceptibilityRow[] {
  return report.bias_susceptibility_table
    .filter((row) => row.agent_id === agentId)
    .sort((a, b) => b.bsi - a.bsi);
}

export function getSecurityRowsForAgent(report: FullReport, agentId: string): SecurityViolationRow[] {
  return report.security_violation_table.filter((row) => row.agent_id === agentId);
}

export function getDeltaRowsForAgent(report: FullReport, agentId: string): SkillsDeltaRow[] {
  return report.skills_mcp_delta_table.filter((row) => row.agent_id === agentId);
}

export function getAllAgentIds(report: FullReport): string[] {
  const ids = new Set(report.per_pillar_aggregate.map((row) => row.agent_id));
  return Array.from(ids).sort();
}
