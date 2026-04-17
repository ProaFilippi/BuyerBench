export interface PillarAggregate {
  agent_id: string;
  pillar: string;
  mean_score: number;
  std: number;
  min: number;
  max: number;
  n_scenarios: number;
}

export interface MetricRow {
  agent_id: string;
  metric: string;
  mean: number;
  min: number;
  max: number;
}

export interface BiasSusceptibilityRow {
  bias_type: string;
  agent_id: string;
  mode: string;
  bsi: number;
  decision_changed: boolean;
  pair_id: string;
}

export interface SecurityViolationRow {
  scenario_id: string;
  agent_id: string;
  compliance_adherence_rate: number;
  security_violation_frequency: number;
  score: number;
}

export interface SkillsDeltaRow {
  family: string;
  mode: string;
  agent_id: string;
  pillar: string;
  baseline_score: number;
  variant_score: number;
  delta: number;
}

export interface ScenarioResult {
  agent_id: string;
  scenario_id: string;
  pillar: string;
  score: number;
  overall_pass: boolean;
  violations: string[];
  notes: string;
  metrics: Record<string, number>;
  raw_output: string;
  decisions: Record<string, unknown>;
  timestamp: string | null;
  is_error: boolean;
}

export interface FullReport {
  generated_at: string;
  experiment_dir: string;
  per_pillar_aggregate: PillarAggregate[];
  per_metric_breakdown: Record<string, MetricRow[]>;
  bias_susceptibility_table: BiasSusceptibilityRow[];
  security_violation_table: SecurityViolationRow[];
  skills_mcp_delta_table: SkillsDeltaRow[];
  scenario_results: ScenarioResult[];
}

/** Derived type for homepage rankings — computed from per_pillar_aggregate */
export interface AgentSummary {
  agent_id: string;
  pillar1_score: number | null;
  pillar2_score: number | null;
  pillar3_score: number | null;
  overall_score: number;
  n_scenarios_total: number;
}
