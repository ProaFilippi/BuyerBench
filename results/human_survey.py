"""Human comparison survey harness for BuyerBench Pillar 2 (UPGRADE-13).

Provides three capabilities:

1. **Survey export** — convert :class:`~buyerbench.models.Scenario` objects into
   clean, human-readable vignettes and export them as a Qualtrics QSF JSON file
   suitable for upload to Qualtrics or a compatible survey platform.

2. **Response ingestion** — parse a Prolific/Qualtrics response CSV into
   :class:`HumanObservation` records, one row per subject per scenario.

3. **Human BSI computation** — aggregate observations into
   :class:`HumanCellAggregate` cells and compute a frequency-based Bias
   Susceptibility Index comparable to the LLM BSI in
   :mod:`evaluators.pillar2`, enabling direct human/LLM comparison via
   :func:`compare_human_llm_bsi`.

Typical usage::

    from results.human_survey import (
        export_scenario_to_survey,
        export_scenarios_to_qualtrics,
        parse_prolific_csv,
        aggregate_human_cells,
        compute_human_bsi_from_survey,
        compare_human_llm_bsi,
    )

    # Export a batch of scenarios to Qualtrics QSF
    from harness.loader import load_all_scenarios
    scenarios = [s for s in load_all_scenarios("scenarios") if s.pillar.value == "PILLAR2"]
    export_scenarios_to_qualtrics(scenarios, "survey/buyerbench-p2-survey.json")

    # After collecting responses, parse Prolific CSV
    observations = parse_prolific_csv(
        "survey/prolific_responses.csv",
        scenario_col="scenario_id",
        choice_col="Q1_supplier",
    )

    # Aggregate and compare with LLM cells
    from harness.loader import load_all_scenarios
    scenario_map = {s.id: s for s in load_all_scenarios("scenarios")}
    human_cells = aggregate_human_cells(observations, scenario_map)

    from results.aggregate_cells import aggregate_cells_from_dir
    llm_report = aggregate_cells_from_dir("results/my-experiment")
    llm_index = {c.cell_id: c for c in llm_report.cells}

    for cell in human_cells:
        baseline_cell = next((c for c in human_cells if ...), None)
        llm_cell = llm_index.get(...)
        comparison = compare_human_llm_bsi(cell, llm_cell)
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from buyerbench.models import Scenario
    from results.aggregate_cells import CellAggregate


# ── Survey vignette export ────────────────────────────────────────────────────

# Human-readable preamble replacing the LLM system preamble.
# Deliberately avoids any mention of AI, benchmarks, or evaluation.
_SURVEY_PREAMBLE = (
    "You are a procurement manager reviewing supplier options for your organisation. "
    "Please read the information below carefully and select the supplier you would choose."
)

# ── Attention check questions ─────────────────────────────────────────────────

ATTENTION_CHECK_QUESTIONS: list[dict[str, Any]] = [
    {
        "attn_id": "ATTN1",
        "question_text": (
            "<b>Attention check</b><br><br>"
            "This question is to confirm you are reading carefully.<br><br>"
            "Two suppliers are quoted for the same component:<br>"
            "• Supplier X: <b>$12.00</b> per unit<br>"
            "• Supplier Y: <b>$89.00</b> per unit<br><br>"
            "Please select the supplier with the <b>lower unit price</b>."
        ),
        "choices": [
            "Supplier X — $12.00 per unit",
            "Supplier Y — $89.00 per unit",
        ],
        "correct_choice": "Supplier X — $12.00 per unit",
    },
    {
        "attn_id": "ATTN2",
        "question_text": (
            "<b>Attention confirmation</b><br><br>"
            "To confirm you have read each question carefully, "
            "please select <b>'I confirm I have read each question'</b> "
            "from the options below."
        ),
        "choices": [
            "I confirm I have read each question",
            "I have not read the questions carefully",
        ],
        "correct_choice": "I confirm I have read each question",
    },
]


def _build_attn_check_element(
    attn_check: dict[str, Any],
    survey_id: str,
    qid: str,
) -> dict[str, Any]:
    """Build a single Qualtrics SQ element for an attention check question."""
    choices: dict[str, dict[str, str]] = {}
    choice_order: list[int] = []
    for ci, option in enumerate(attn_check["choices"], start=1):
        choices[str(ci)] = {"Display": option}
        choice_order.append(ci)

    return {
        "SurveyID": survey_id,
        "Element": "SQ",
        "PrimaryAttribute": qid,
        "SecondaryAttribute": f"attention_check_{attn_check['attn_id']}",
        "Payload": {
            "QuestionText": attn_check["question_text"],
            "DataExportTag": qid,
            "QuestionType": "MC",
            "Selector": "SAVR",
            "SubSelector": "TX",
            "Configuration": {"QuestionDescriptionOption": "UseText"},
            "Choices": choices,
            "ChoiceOrder": choice_order,
            "Validation": {
                "Settings": {
                    "ForceResponse": "ON",
                    "ForceResponseType": "ON",
                    "Type": "None",
                }
            },
            "Language": [],
            "NextChoiceId": len(choices) + 1,
            "NextAnswerId": 1,
            "_buyerbench": {
                "scenario_id": f"attention_check_{attn_check['attn_id']}",
                "variant": "ATTENTION_CHECK",
                "variant_pair_id": None,
                "optimal_choice": attn_check["correct_choice"],
                "choices": attn_check["choices"],
                "is_attention_check": True,
            },
        },
    }


def export_scenarios_to_qualtrics_with_attention_checks(
    scenarios: "list[Scenario]",
    output_path: "str | Path",
    *,
    survey_name: str = "Procurement Decision Study",
    attention_check_positions: "list[int] | None" = None,
) -> "Path":
    """Export scenarios as Qualtrics QSF with embedded attention checks.

    Identical to :func:`export_scenarios_to_qualtrics` but interleaves
    :data:`ATTENTION_CHECK_QUESTIONS` at the specified 0-indexed positions
    within the final question sequence.

    Args:
        scenarios:                 Scenarios to include (one block each).
        output_path:               Destination QSF JSON file path.
        survey_name:               Survey name shown in Qualtrics.
        attention_check_positions: 0-indexed positions in the *final* question
                                   list at which to insert each attention check.
                                   Must equal ``len(ATTENTION_CHECK_QUESTIONS)``.
                                   Defaults to ``[2, 5]`` (after scenarios 2 and
                                   4 in a 5-scenario survey, yielding order
                                   S1 S2 ATTN1 S3 S4 ATTN2 S5).

    Returns:
        :class:`~pathlib.Path` of the written QSF file.
    """
    if attention_check_positions is None:
        attention_check_positions = [2, 5]

    if len(attention_check_positions) != len(ATTENTION_CHECK_QUESTIONS):
        raise ValueError(
            f"attention_check_positions must have {len(ATTENTION_CHECK_QUESTIONS)} entries, "
            f"got {len(attention_check_positions)}"
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    survey_id = "SV_BuyerBenchP2"

    # Build interleaved sequence of scenario vignettes + attention check markers
    # marker: {"type": "attn", "attn_check": dict}
    # scenario: {"type": "scenario", "scenario": Scenario}
    interleaved: list[dict[str, Any]] = []
    attn_positions_sorted = sorted(
        zip(attention_check_positions, ATTENTION_CHECK_QUESTIONS),
        key=lambda x: x[0],
    )
    attn_iter = iter(attn_positions_sorted)
    next_attn = next(attn_iter, None)

    scenario_qids: list[str] = []
    attn_qids: list[str] = []
    all_elements: list[dict[str, Any]] = []
    block_refs: list[dict[str, str]] = []

    final_idx = 0
    scenario_iter = iter(enumerate(scenarios, start=1))

    # Build final ordered list of (item_type, content)
    ordered_items: list[tuple[str, Any]] = []
    sc_list = list(scenarios)
    attn_targets = list(zip(attention_check_positions, ATTENTION_CHECK_QUESTIONS))
    attn_targets.sort(key=lambda x: x[0])

    # Insert scenarios and attention checks by target index
    sc_queue = list(sc_list)
    attn_queue = list(attn_targets)  # (position, attn_check)
    final_position = 0

    while sc_queue or attn_queue:
        # Check if we should insert an attention check at this position
        while attn_queue and attn_queue[0][0] == final_position:
            _, attn_check = attn_queue.pop(0)
            ordered_items.append(("attn", attn_check))
            final_position += 1
        if sc_queue:
            ordered_items.append(("scenario", sc_queue.pop(0)))
            final_position += 1

    # Flush remaining attention checks (positions beyond all scenarios)
    for _, attn_check in attn_queue:
        ordered_items.append(("attn", attn_check))

    # Now build QSF elements
    sc_idx = 0
    attn_counter = 0
    for item_type, content in ordered_items:
        if item_type == "scenario":
            sc_idx += 1
            qid = f"QID{sc_idx}"
            vignette = export_scenario_to_survey(content)
            choices: dict[str, dict[str, str]] = {}
            choice_order: list[int] = []
            for ci, option in enumerate(vignette["choices"], start=1):
                choices[str(ci)] = {"Display": option}
                choice_order.append(ci)

            question_text = (
                f"<b>{vignette['title']}</b><br><br>"
                f"{vignette['preamble']}<br><br>"
                f"<b>Scenario:</b><br>"
                f"{vignette['context_text'].replace(chr(10), '<br>')}<br><br>"
            )
            if vignette["constraints_text"]:
                question_text += (
                    f"<b>Requirements:</b> {vignette['constraints_text']}<br><br>"
                )
            question_text += f"<b>{vignette['question']}</b>"

            elem = {
                "SurveyID": survey_id,
                "Element": "SQ",
                "PrimaryAttribute": qid,
                "SecondaryAttribute": content.id,
                "Payload": {
                    "QuestionText": question_text,
                    "DataExportTag": qid,
                    "QuestionType": "MC",
                    "Selector": "SAVR",
                    "SubSelector": "TX",
                    "Configuration": {"QuestionDescriptionOption": "UseText"},
                    "Choices": choices,
                    "ChoiceOrder": choice_order,
                    "Validation": {
                        "Settings": {
                            "ForceResponse": "ON",
                            "ForceResponseType": "ON",
                            "Type": "None",
                        }
                    },
                    "Language": [],
                    "NextChoiceId": len(choices) + 1,
                    "NextAnswerId": 1,
                    "_buyerbench": {
                        "scenario_id": content.id,
                        "variant": content.variant.value,
                        "variant_pair_id": content.variant_pair_id,
                        "optimal_choice": vignette["optimal_choice"],
                        "choices": vignette["choices"],
                    },
                },
            }
            all_elements.append(elem)
            block_refs.append({"Type": "Question", "QuestionID": qid})
            scenario_qids.append(qid)
        else:  # attn
            attn_counter += 1
            qid = f"ATTN{attn_counter}"
            elem = _build_attn_check_element(content, survey_id, qid)
            all_elements.append(elem)
            block_refs.append({"Type": "Question", "QuestionID": qid})
            attn_qids.append(qid)

    block_element: dict[str, Any] = {
        "SurveyID": survey_id,
        "Element": "BL",
        "PrimaryAttribute": "Survey Blocks",
        "SecondaryAttribute": None,
        "Payload": {
            "0": {
                "Type": "Default",
                "Description": "Procurement Vignettes",
                "ID": "BL_default",
                "BlockElements": block_refs,
                "Options": {"BlockLocking": "false", "RandomizeQuestions": "false"},
            }
        },
    }

    survey_entry: dict[str, Any] = {
        "SurveyID": survey_id,
        "SurveyName": survey_name,
        "SurveyDescription": (
            "Online survey study of procurement decision-making in organisations."
        ),
        "SurveyStatus": "Inactive",
        "SurveyStartDate": "",
        "SurveyExpirationDate": "",
        "SurveyCreationDate": datetime.now(timezone.utc).isoformat(),
        "CreatorID": "buyerbench",
        "LastModified": datetime.now(timezone.utc).isoformat(),
        "LastAccessed": "",
        "LastActivated": "",
        "Deleted": None,
    }

    qsf: dict[str, Any] = {
        "SurveyEntry": survey_entry,
        "SurveyElements": [block_element] + all_elements,
    }

    output_path.write_text(json.dumps(qsf, indent=2))
    return output_path


def generate_survey_manifest(
    version_a_scenarios: "list[Scenario]",
    version_b_scenarios: "list[Scenario]",
    *,
    bias_mapping: "dict[str, dict[str, str]] | None" = None,
    attention_check_positions: "list[int] | None" = None,
    n_subjects_target: int = 100,
    n_per_version: int = 50,
) -> dict[str, Any]:
    """Build the survey manifest dict for result parsing.

    The manifest records which scenario IDs appear in each survey version, the
    attention check positions, and column conventions for parsing Prolific CSV
    exports via :func:`parse_prolific_csv`.

    Args:
        version_a_scenarios:       Scenarios in Version A (BASELINE).
        version_b_scenarios:       Scenarios in Version B (TREATMENT).
        bias_mapping:              ``{bias_type: {baseline: id, treatment: id}}``.
        attention_check_positions: Positions (0-indexed in final question list)
                                   where attention checks are inserted.
        n_subjects_target:         Total subjects planned.
        n_per_version:             Subjects per survey version.

    Returns:
        Dict ready for ``json.dumps``.
    """
    if attention_check_positions is None:
        attention_check_positions = [2, 5]

    def _scenario_entry(sc: "Scenario", position: int) -> dict[str, Any]:
        return {
            "position": position,
            "scenario_id": sc.id,
            "bias_type": (
                "-".join(sc.variant_pair_id.split("-")[2:])
                if sc.variant_pair_id and len(sc.variant_pair_id.split("-")) >= 3
                else None
            ),
            "variant": sc.variant.value,
            "variant_pair_id": sc.variant_pair_id,
            "optimal_choice": next(iter(sc.expected_optimal.values()), None),
        }

    version_a_entries = [
        _scenario_entry(sc, i + 1) for i, sc in enumerate(version_a_scenarios)
    ]
    version_b_entries = [
        _scenario_entry(sc, i + 1) for i, sc in enumerate(version_b_scenarios)
    ]
    attn_entries = [
        {
            "position": pos,
            "qid": f"ATTN{i + 1}",
            "attn_id": aq["attn_id"],
            "correct_choice": aq["correct_choice"],
        }
        for i, (pos, aq) in enumerate(
            sorted(zip(attention_check_positions, ATTENTION_CHECK_QUESTIONS), key=lambda x: x[0])
        )
    ]

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "design": {
            "n_subjects_target": n_subjects_target,
            "n_per_version": n_per_version,
            "n_bias_types": len(version_a_scenarios),
            "n_scenarios_per_subject": len(version_a_scenarios),
            "between_subjects_variants": True,
            "within_subjects_bias_types": True,
        },
        "bias_mapping": bias_mapping or {},
        "version_a_baseline": version_a_entries,
        "version_b_treatment": version_b_entries,
        "attention_checks": attn_entries,
        "attention_check_exclusion_rule": (
            "Exclude subjects who fail ≥1 attention check "
            "(attention_check_passed=False in aggregated data)."
        ),
        "prolific_csv_columns": {
            "subject_id_col": "Participant id",
            "scenario_col": "scenario_id",
            "choice_col": "selected_choice",
            "variant_col": "variant",
            "variant_pair_id_col": "variant_pair_id",
            "bias_category_col": "bias_category",
            "optimal_choice_col": "optimal_choice",
            "response_time_col": "response_time_ms",
            "attention_check_col": "attention_check_passed",
        },
    }


def _format_context_plain(context: dict[str, Any]) -> list[str]:
    """Render context dict as plain human-readable text (no markdown fences).

    List-of-dicts become simple numbered tables; plain dicts become bullet
    lists; scalars become inline text.  No system/AI language is included.
    """
    lines: list[str] = []
    for key, value in context.items():
        heading = key.replace("_", " ").title()
        if isinstance(value, list) and value and isinstance(value[0], dict):
            lines.append(f"{heading}:")
            cols = list(value[0].keys())
            # header row
            lines.append("  " + " | ".join(c.replace("_", " ").title() for c in cols))
            lines.append("  " + " | ".join(["---"] * len(cols)))
            for row in value:
                cells = [str(row.get(c, "")) for c in cols]
                lines.append("  " + " | ".join(cells))
        elif isinstance(value, list):
            lines.append(f"{heading}:")
            for item in value:
                lines.append(f"  • {item}")
        elif isinstance(value, dict):
            lines.append(f"{heading}:")
            for k, v in value.items():
                label = k.replace("_", " ").title()
                lines.append(f"  • {label}: {v}")
        else:
            lines.append(f"{heading}: {value}")
    return lines


def _extract_choice_options(scenario: "Scenario") -> list[str]:
    """Return the ordered list of supplier/option names from *scenario*.

    Looks first in ``scenario.context["suppliers"]`` (list of dicts with a
    ``"name"`` key), then in other list-of-dicts context entries, then falls
    back to the keys of ``scenario.expected_optimal``.
    """
    # Prefer suppliers list
    suppliers = scenario.context.get("suppliers", [])
    if suppliers and isinstance(suppliers, list) and isinstance(suppliers[0], dict):
        names = [row.get("name") or row.get("vendor") or row.get("contract") for row in suppliers]
        names = [str(n) for n in names if n is not None]
        if names:
            return names

    # Try any list-of-dicts context entry with a name/vendor/contract key
    for key, value in scenario.context.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            row = value[0]
            for field in ("name", "vendor", "contract", "supplier"):
                if field in row:
                    return [str(r[field]) for r in value if field in r]

    # Fallback: return the expected optimal value as the only "correct" option
    opt_key = next(iter(scenario.expected_optimal), None)
    if opt_key:
        return [str(scenario.expected_optimal[opt_key])]

    return []


def export_scenario_to_survey(scenario: "Scenario") -> dict[str, Any]:
    """Convert *scenario* into a human-readable survey vignette dict.

    The returned dict contains:

    - ``scenario_id`` — identifier for result mapping
    - ``variant`` — the scenario variant (e.g. ``"BASELINE"``)
    - ``variant_pair_id`` — pair grouping key
    - ``bias_category`` — e.g. ``"anchoring"``
    - ``title`` — plain-English procurement context title
    - ``preamble`` — neutral role-framing text (no benchmark language)
    - ``context_text`` — multi-line string of context rendered for humans
    - ``question`` — forced-choice question text
    - ``choices`` — ordered list of option names (supplier names, etc.)
    - ``optimal_choice`` — the expected optimal choice (for result scoring)
    - ``constraints_text`` — human-readable constraints paragraph

    All BuyerBench-specific and AI-evaluation language is stripped from the
    vignette to prevent demand effects in human subjects.
    """
    # Infer bias_category from variant_pair_id naming convention
    bias_category: str | None = None
    if scenario.variant_pair_id:
        parts = scenario.variant_pair_id.split("-")
        if len(parts) >= 3:
            bias_category = "-".join(parts[2:])

    context_lines = _format_context_plain(scenario.context)
    context_text = "\n".join(context_lines)

    choices = _extract_choice_options(scenario)

    # Determine the question key from expected_optimal
    opt_keys = list(scenario.expected_optimal.keys())
    question_key = opt_keys[0] if opt_keys else "supplier"
    optimal_choice = str(scenario.expected_optimal.get(question_key, ""))

    # Build constraints paragraph — filter out scoring/algorithm language
    constraints_text = "; ".join(scenario.constraints) if scenario.constraints else ""

    return {
        "scenario_id": scenario.id,
        "variant": scenario.variant.value,
        "variant_pair_id": scenario.variant_pair_id,
        "bias_category": bias_category,
        "title": scenario.title,
        "preamble": _SURVEY_PREAMBLE,
        "context_text": context_text,
        "question": f"Which {question_key} would you select?",
        "choices": choices,
        "optimal_choice": optimal_choice,
        "constraints_text": constraints_text,
    }


def export_scenarios_to_qualtrics(
    scenarios: list["Scenario"],
    output_path: str | Path,
    survey_name: str = "Procurement Decision Study",
) -> Path:
    """Export *scenarios* as a Qualtrics QSF-format JSON file.

    Each scenario becomes one multiple-choice block.  The QSF structure
    follows the Qualtrics Survey File format (version 3.0):
    - ``SurveyEntry`` — top-level metadata
    - ``SurveyElements`` — one block descriptor + one question per scenario
      + one response set element

    The output file is importable directly via Qualtrics > Projects >
    Create Project > Import a QSF file.

    Args:
        scenarios:    List of :class:`~buyerbench.models.Scenario` to include.
        output_path:  Path for the output JSON file.
        survey_name:  Survey name shown in Qualtrics (default: "Procurement
                      Decision Study" — no benchmark language).

    Returns:
        :class:`~pathlib.Path` of the written QSF file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    survey_id = "SV_BuyerBenchP2"
    block_elements: list[dict[str, Any]] = []
    question_elements: list[dict[str, Any]] = []

    for idx, scenario in enumerate(scenarios, start=1):
        vignette = export_scenario_to_survey(scenario)
        qid = f"QID{idx}"
        block_elements.append({"Type": "Question", "QuestionID": qid})

        # Build choice dict (1-indexed, Qualtrics requires string keys)
        choices: dict[str, dict[str, str]] = {}
        choice_order: list[int] = []
        for ci, option in enumerate(vignette["choices"], start=1):
            choices[str(ci)] = {"Display": option}
            choice_order.append(ci)

        question_text = (
            f"<b>{vignette['title']}</b><br><br>"
            f"{vignette['preamble']}<br><br>"
            f"<b>Scenario:</b><br>"
            f"{vignette['context_text'].replace(chr(10), '<br>')}<br><br>"
        )
        if vignette["constraints_text"]:
            question_text += (
                f"<b>Requirements:</b> {vignette['constraints_text']}<br><br>"
            )
        question_text += f"<b>{vignette['question']}</b>"

        question_elements.append({
            "SurveyID": survey_id,
            "Element": "SQ",
            "PrimaryAttribute": qid,
            "SecondaryAttribute": scenario.id,
            "Payload": {
                "QuestionText": question_text,
                "DataExportTag": qid,
                "QuestionType": "MC",
                "Selector": "SAVR",
                "SubSelector": "TX",
                "Configuration": {"QuestionDescriptionOption": "UseText"},
                "Choices": choices,
                "ChoiceOrder": choice_order,
                "Validation": {
                    "Settings": {
                        "ForceResponse": "ON",
                        "ForceResponseType": "ON",
                        "Type": "None",
                    }
                },
                "Language": [],
                "NextChoiceId": len(choices) + 1,
                "NextAnswerId": 1,
                # Store metadata for result mapping
                "_buyerbench": {
                    "scenario_id": scenario.id,
                    "variant": scenario.variant.value,
                    "variant_pair_id": scenario.variant_pair_id,
                    "optimal_choice": vignette["optimal_choice"],
                    "choices": vignette["choices"],
                },
            },
        })

    # Block element wrapping all questions
    block_element = {
        "SurveyID": survey_id,
        "Element": "BL",
        "PrimaryAttribute": "Survey Blocks",
        "SecondaryAttribute": None,
        "Payload": {
            "0": {
                "Type": "Default",
                "Description": "Procurement Vignettes",
                "ID": "BL_default",
                "BlockElements": block_elements,
                "Options": {"BlockLocking": "false", "RandomizeQuestions": "false"},
            }
        },
    }

    survey_entry = {
        "SurveyID": survey_id,
        "SurveyName": survey_name,
        "SurveyDescription": (
            "Online survey study of procurement decision-making in organisations."
        ),
        "SurveyStatus": "Inactive",
        "SurveyStartDate": "",
        "SurveyExpirationDate": "",
        "SurveyCreationDate": datetime.now(timezone.utc).isoformat(),
        "CreatorID": "buyerbench",
        "LastModified": datetime.now(timezone.utc).isoformat(),
        "LastAccessed": "",
        "LastActivated": "",
        "Deleted": None,
    }

    qsf = {
        "SurveyEntry": survey_entry,
        "SurveyElements": [block_element] + question_elements,
    }

    output_path.write_text(json.dumps(qsf, indent=2))
    return output_path


# ── HumanObservation schema ───────────────────────────────────────────────────


class HumanObservation(BaseModel):
    """A single human subject's response to one survey scenario.

    Parallel to :class:`~buyerbench.models.AgentResponse` but adapted for
    human survey data — no token counts or API costs, but includes
    Prolific-specific fields such as ``response_time_ms`` and
    ``attention_check_passed``.
    """

    subject_id: str
    """Prolific participant ID (anonymised)."""

    scenario_id: str
    """Scenario identifier, matching ``Scenario.id``."""

    variant_pair_id: str | None = None
    """Variant pair grouping key (from ``Scenario.variant_pair_id``)."""

    variant: str
    """ScenarioVariant value, e.g. ``"BASELINE"`` or ``"ANCHOR_HIGH"``."""

    bias_category: str | None = None
    """Bias category inferred from variant_pair_id, e.g. ``"anchoring"``."""

    selected_choice: str
    """The option the subject selected (supplier name, contract name, etc.)."""

    optimal_choice: str
    """The ground-truth optimal choice for this scenario."""

    choice_is_correct: bool = False
    """``True`` if ``selected_choice == optimal_choice`` (case-insensitive)."""

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    """UTC timestamp of the response submission."""

    response_time_ms: float | None = None
    """Time from question display to submission in milliseconds."""

    attention_check_passed: bool | None = None
    """``True`` if the subject passed all attention checks; ``None`` if not assessed."""

    @classmethod
    def from_row(
        cls,
        *,
        subject_id: str,
        scenario_id: str,
        selected_choice: str,
        optimal_choice: str,
        variant: str,
        variant_pair_id: str | None = None,
        bias_category: str | None = None,
        timestamp: datetime | None = None,
        response_time_ms: float | None = None,
        attention_check_passed: bool | None = None,
    ) -> "HumanObservation":
        """Construct from parsed survey row fields."""
        choice_is_correct = (
            selected_choice.strip().lower() == optimal_choice.strip().lower()
        )
        return cls(
            subject_id=subject_id,
            scenario_id=scenario_id,
            variant_pair_id=variant_pair_id,
            variant=variant,
            bias_category=bias_category,
            selected_choice=selected_choice,
            optimal_choice=optimal_choice,
            choice_is_correct=choice_is_correct,
            timestamp=timestamp or datetime.now(timezone.utc),
            response_time_ms=response_time_ms,
            attention_check_passed=attention_check_passed,
        )


# ── HumanCellAggregate schema ─────────────────────────────────────────────────


class HumanCellAggregate(BaseModel):
    """Aggregated statistics for a (scenario_id, variant) human survey cell.

    Parallel to :class:`~results.aggregate_cells.CellAggregate` but computed
    from human subject frequency data rather than repeated LLM runs.

    Because human subjects are sampled between-subjects across variants
    (each subject sees only one variant per bias type), the aggregation is
    over *subjects*, not over repeated runs by the same agent.
    """

    cell_id: str
    """Unique string key: ``{variant_pair_id or scenario_id}__{variant}``."""

    scenario_id: str
    variant_pair_id: str | None = None
    variant: str
    bias_category: str | None = None

    n_subjects: int
    """Total number of subjects who saw this cell (including failed attention checks)."""

    n_valid_subjects: int
    """Subjects who passed all attention checks (used as denominator for metrics)."""

    choice_rate_optimal: float
    """Fraction of valid subjects who selected the optimal choice."""

    choice_rate_distribution: dict[str, int] = Field(default_factory=dict)
    """Option name → number of valid subjects who selected it."""

    mean_bsi: float
    """Aggregate BSI for the cell = ``1.0 - choice_rate_optimal``.

    Under the frequency-based formulation: if *P* is the fraction of subjects
    who chose the optimal option, BSI = 1 − P.  A perfectly rational group has
    BSI = 0.0; a completely biased group has BSI = 1.0.  This mirrors the LLM
    per-run BSI formula (0 if optimal chosen, 1 if not) averaged over N subjects.
    """

    ci_lower_95: float
    """Lower bound of the 95 % Wilson score CI for choice_rate_optimal."""

    ci_upper_95: float
    """Upper bound of the 95 % Wilson score CI for choice_rate_optimal."""

    treatment_effect_vs_baseline: float | None = None
    """For non-BASELINE cells: ``mean_bsi(treatment) - mean_bsi(baseline)``."""


class HumanCellReport(BaseModel):
    """Full human survey aggregate report."""

    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    n_observations: int
    n_cells: int
    cells: list[HumanCellAggregate] = Field(default_factory=list)


# ── HumanComparisonResult schema ──────────────────────────────────────────────


class HumanComparisonResult(BaseModel):
    """Statistical comparison of human BSI vs LLM BSI for a single cell.

    Implements the H10 test from the research design: independent two-sample
    comparison of ``mean_bsi(LLM)`` versus ``mean_bsi(humans)`` for the same
    scenario variant.
    """

    cell_id: str
    """Common cell identifier (variant_pair_id + variant)."""

    bias_category: str | None = None
    variant: str

    human_mean_bsi: float
    llm_mean_bsi: float

    bsi_difference: float
    """``human_mean_bsi - llm_mean_bsi``; positive means humans are more biased."""

    cohens_d: float
    """Effect size estimate for the BSI difference.

    Computed as ``bsi_difference / pooled_std`` where pooled_std is derived
    from the binomial variance of the human rate and the empirical std of the
    LLM cell.  Returns 0.0 if pooled_std is zero.
    """

    ci_lower_95: float
    """Lower bound of 95 % CI for ``bsi_difference`` (normal approximation)."""

    ci_upper_95: float
    """Upper bound of 95 % CI for ``bsi_difference`` (normal approximation)."""

    n_human: int
    """Number of valid human subjects in this cell."""

    n_llm: int
    """Number of valid LLM runs in this cell."""


# ── CI helpers ────────────────────────────────────────────────────────────────


def _wilson_score_ci_95(k: int, n: int) -> tuple[float, float]:
    """95 % Wilson score interval for a proportion k/n.

    Preferred over normal approximation for small n or extreme proportions.
    Returns ``(lower, upper)`` clamped to ``[0.0, 1.0]``.
    For n=0, returns ``(0.0, 0.0)``.
    """
    if n == 0:
        return (0.0, 0.0)
    z = 1.96  # 95 % two-tailed z
    p_hat = k / n
    centre = (p_hat + z * z / (2 * n)) / (1 + z * z / n)
    half_width = (z / (1 + z * z / n)) * math.sqrt(
        p_hat * (1 - p_hat) / n + z * z / (4 * n * n)
    )
    return (max(0.0, centre - half_width), min(1.0, centre + half_width))


def _difference_ci_95(
    mean_diff: float,
    var_human: float,
    var_llm: float,
    n_human: int,
    n_llm: int,
) -> tuple[float, float]:
    """95 % CI for a difference of two independent means (normal approximation).

    Uses the Satterthwaite-style combined standard error.
    """
    se = math.sqrt(var_human / max(1, n_human) + var_llm / max(1, n_llm))
    margin = 1.96 * se
    return (mean_diff - margin, mean_diff + margin)


# ── CSV ingestion ─────────────────────────────────────────────────────────────


def parse_prolific_csv(
    csv_path: str | Path,
    *,
    subject_id_col: str = "Participant id",
    scenario_col: str = "scenario_id",
    choice_col: str = "selected_choice",
    variant_col: str | None = "variant",
    variant_pair_id_col: str | None = "variant_pair_id",
    bias_category_col: str | None = "bias_category",
    optimal_choice_col: str | None = "optimal_choice",
    response_time_col: str | None = None,
    attention_check_col: str | None = None,
    scenario_map: dict[str, Any] | None = None,
) -> list[HumanObservation]:
    """Parse a Prolific/Qualtrics response CSV into :class:`HumanObservation` records.

    The CSV is expected to have one row per subject per scenario response.
    Column names are configurable to accommodate both Prolific export format
    (which includes a ``"Participant id"`` column) and custom flat exports.

    Args:
        csv_path:            Path to the response CSV file.
        subject_id_col:      Column containing the Prolific participant ID.
        scenario_col:        Column identifying the scenario (``scenario_id``).
        choice_col:          Column containing the subject's chosen option name.
        variant_col:         Column identifying the ScenarioVariant value.
                             If ``None``, variant is left as ``"UNKNOWN"``.
        variant_pair_id_col: Column for the variant pair grouping key.
        bias_category_col:   Column for the bias category label.
        optimal_choice_col:  Column for the ground-truth optimal choice.
                             If ``None``, optimal_choice is looked up from
                             *scenario_map* if provided.
        response_time_col:   Column for time-on-task in milliseconds.
        attention_check_col: Column for attention check result (``"1"``/``"true"``
                             → passed; ``"0"``/``"false"`` → failed).
        scenario_map:        Optional ``{scenario_id: Scenario}`` dict used to
                             look up ``optimal_choice``, ``variant``, and
                             ``variant_pair_id`` when the corresponding columns
                             are absent from the CSV.

    Returns:
        List of :class:`HumanObservation` records, one per CSV data row.
    """
    csv_path = Path(csv_path)
    observations: list[HumanObservation] = []

    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            subject_id = row.get(subject_id_col, "").strip()
            scenario_id = row.get(scenario_col, "").strip()
            selected_choice = row.get(choice_col, "").strip()

            if not subject_id or not scenario_id or not selected_choice:
                continue  # skip incomplete rows

            variant = (
                row.get(variant_col, "").strip() if variant_col else "UNKNOWN"
            ) or "UNKNOWN"
            pair_id = (
                row.get(variant_pair_id_col, "").strip()
                if variant_pair_id_col
                else None
            ) or None
            bias_cat = (
                row.get(bias_category_col, "").strip()
                if bias_category_col
                else None
            ) or None

            optimal_choice = ""
            if optimal_choice_col:
                optimal_choice = row.get(optimal_choice_col, "").strip()

            # Fall back to scenario_map lookup for metadata
            if scenario_map and scenario_id in scenario_map:
                sc = scenario_map[scenario_id]
                if not optimal_choice:
                    opt_key = next(iter(sc.expected_optimal), None)
                    if opt_key:
                        optimal_choice = str(sc.expected_optimal[opt_key])
                if variant == "UNKNOWN":
                    variant = sc.variant.value
                if pair_id is None:
                    pair_id = sc.variant_pair_id
                if bias_cat is None and sc.variant_pair_id:
                    parts = sc.variant_pair_id.split("-")
                    if len(parts) >= 3:
                        bias_cat = "-".join(parts[2:])

            # Response time
            rt_ms: float | None = None
            if response_time_col and row.get(response_time_col):
                try:
                    rt_ms = float(row[response_time_col])
                except ValueError:
                    pass

            # Attention check
            att: bool | None = None
            if attention_check_col and row.get(attention_check_col):
                val = row[attention_check_col].strip().lower()
                if val in ("1", "true", "yes", "pass", "passed"):
                    att = True
                elif val in ("0", "false", "no", "fail", "failed"):
                    att = False

            obs = HumanObservation.from_row(
                subject_id=subject_id,
                scenario_id=scenario_id,
                selected_choice=selected_choice,
                optimal_choice=optimal_choice,
                variant=variant,
                variant_pair_id=pair_id,
                bias_category=bias_cat,
                response_time_ms=rt_ms,
                attention_check_passed=att,
            )
            observations.append(obs)

    return observations


def observations_to_csv(
    observations: list[HumanObservation],
    output_path: str | Path,
) -> Path:
    """Serialise *observations* to a CSV file and return the path.

    The CSV uses the same column layout expected by :func:`parse_prolific_csv`
    with default column names, making round-trips lossless (modulo float precision).

    Args:
        observations: List of :class:`HumanObservation` records to write.
        output_path:  Destination file path (parent dirs are created if absent).

    Returns:
        :class:`~pathlib.Path` of the written file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Participant id",
        "scenario_id",
        "variant",
        "variant_pair_id",
        "bias_category",
        "selected_choice",
        "optimal_choice",
        "choice_is_correct",
        "response_time_ms",
        "attention_check_passed",
        "timestamp",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for obs in observations:
            writer.writerow({
                "Participant id": obs.subject_id,
                "scenario_id": obs.scenario_id,
                "variant": obs.variant,
                "variant_pair_id": obs.variant_pair_id or "",
                "bias_category": obs.bias_category or "",
                "selected_choice": obs.selected_choice,
                "optimal_choice": obs.optimal_choice,
                "choice_is_correct": str(obs.choice_is_correct).lower(),
                "response_time_ms": obs.response_time_ms if obs.response_time_ms is not None else "",
                "attention_check_passed": (
                    "" if obs.attention_check_passed is None
                    else str(obs.attention_check_passed).lower()
                ),
                "timestamp": obs.timestamp.isoformat(),
            })

    return output_path


# ── Aggregation ───────────────────────────────────────────────────────────────


def _human_cell_key(obs: HumanObservation) -> tuple:
    """Group key: ``(variant_pair_id or scenario_id, variant)``."""
    return (obs.variant_pair_id or obs.scenario_id, obs.variant)


def _compute_human_cell_aggregate(
    observations: list[HumanObservation],
    *,
    exclude_failed_attention: bool = True,
) -> HumanCellAggregate:
    """Aggregate *observations* belonging to a single (scenario, variant) cell."""
    first = observations[0]
    pair_group = first.variant_pair_id or first.scenario_id

    valid_obs = [
        o for o in observations
        if not exclude_failed_attention or o.attention_check_passed is not False
    ]
    n_total = len(observations)
    n_valid = len(valid_obs)

    # Choice frequency
    choice_dist: dict[str, int] = {}
    n_correct = 0
    for obs in valid_obs:
        key = obs.selected_choice
        choice_dist[key] = choice_dist.get(key, 0) + 1
        if obs.choice_is_correct:
            n_correct += 1

    choice_rate_optimal = n_correct / n_valid if n_valid > 0 else 0.0
    mean_bsi = 1.0 - choice_rate_optimal

    ci_lower, ci_upper = _wilson_score_ci_95(n_correct, n_valid)
    # Convert CI on choice_rate_optimal to CI on BSI (BSI = 1 - p)
    bsi_ci_lower = 1.0 - ci_upper
    bsi_ci_upper = 1.0 - ci_lower

    cell_id = f"{pair_group}__{first.variant}"

    return HumanCellAggregate(
        cell_id=cell_id,
        scenario_id=first.scenario_id,
        variant_pair_id=first.variant_pair_id,
        variant=first.variant,
        bias_category=first.bias_category,
        n_subjects=n_total,
        n_valid_subjects=n_valid,
        choice_rate_optimal=choice_rate_optimal,
        choice_rate_distribution=choice_dist,
        mean_bsi=round(mean_bsi, 6),
        ci_lower_95=round(bsi_ci_lower, 6),
        ci_upper_95=round(bsi_ci_upper, 6),
        treatment_effect_vs_baseline=None,
    )


def _add_human_treatment_effects(cells: list[HumanCellAggregate]) -> None:
    """In-place: fill ``treatment_effect_vs_baseline`` for non-BASELINE cells."""
    baseline_index: dict[tuple, HumanCellAggregate] = {}
    for cell in cells:
        if cell.variant == "BASELINE" and cell.variant_pair_id:
            key = (cell.variant_pair_id,)
            baseline_index[key] = cell

    for cell in cells:
        if cell.variant == "BASELINE" or not cell.variant_pair_id:
            continue
        key = (cell.variant_pair_id,)
        baseline = baseline_index.get(key)
        if baseline is not None:
            cell.treatment_effect_vs_baseline = round(
                cell.mean_bsi - baseline.mean_bsi, 6
            )


def aggregate_human_cells(
    observations: list[HumanObservation],
    *,
    exclude_failed_attention: bool = True,
) -> HumanCellReport:
    """Aggregate *observations* into cell-level statistics.

    Groups by ``(variant_pair_id or scenario_id, variant)`` and computes
    ``choice_rate_optimal``, ``mean_bsi``, Wilson score 95 % CI, and
    treatment effects for each cell.

    Args:
        observations:            Flat list of :class:`HumanObservation` from
                                  one or more scenarios and variants.
        exclude_failed_attention: When ``True`` (default), subjects with
                                  ``attention_check_passed == False`` are
                                  excluded from metric calculations (but still
                                  counted in ``n_subjects``).

    Returns:
        :class:`HumanCellReport` with cells sorted by ``(pair_id, variant)``.
    """
    grouped: dict[tuple, list[HumanObservation]] = defaultdict(list)
    for obs in observations:
        grouped[_human_cell_key(obs)].append(obs)

    cells: list[HumanCellAggregate] = []
    for key in sorted(grouped.keys()):
        cell = _compute_human_cell_aggregate(
            grouped[key],
            exclude_failed_attention=exclude_failed_attention,
        )
        cells.append(cell)

    _add_human_treatment_effects(cells)

    return HumanCellReport(
        n_observations=len(observations),
        n_cells=len(cells),
        cells=cells,
    )


# ── Human BSI computation ─────────────────────────────────────────────────────


def compute_human_bsi_from_survey(
    baseline_agg: HumanCellAggregate,
    variant_agg: HumanCellAggregate,
) -> dict[str, Any]:
    """Compute frequency-based Bias Susceptibility Index from two survey cells.

    Human BSI is defined as:
    ``|P(optimal | TREATMENT) - P(optimal | BASELINE)|``

    A positive BSI indicates that the treatment manipulation shifted subjects
    *away* from the optimal choice.  A negative value indicates the treatment
    *improved* optimal selection (counter-bias effect).

    The direction is preserved in ``bsi_signed`` for detection of counter-
    bias effects; ``bias_susceptibility_index`` is the absolute value.

    Args:
        baseline_agg:  Aggregated cell for the BASELINE variant.
        variant_agg:   Aggregated cell for the treatment variant.

    Returns:
        Dict with:
        - ``baseline_scenario_id``
        - ``variant_scenario_id``
        - ``choice_rate_optimal_baseline``: P(optimal | BASELINE)
        - ``choice_rate_optimal_variant``: P(optimal | TREATMENT)
        - ``bsi_signed``: signed difference (baseline_rate - variant_rate)
        - ``bias_susceptibility_index``: absolute value of bsi_signed
        - ``variant_type``: variant name (e.g. ``"ANCHOR_HIGH"``)
        - ``pair_id``: variant_pair_id
    """
    p_baseline = baseline_agg.choice_rate_optimal
    p_variant = variant_agg.choice_rate_optimal

    bsi_signed = p_baseline - p_variant  # positive = treatment made things worse
    bsi_abs = abs(bsi_signed)

    return {
        "baseline_scenario_id": baseline_agg.scenario_id,
        "variant_scenario_id": variant_agg.scenario_id,
        "choice_rate_optimal_baseline": p_baseline,
        "choice_rate_optimal_variant": p_variant,
        "bsi_signed": round(bsi_signed, 6),
        "bias_susceptibility_index": round(bsi_abs, 6),
        "variant_type": variant_agg.variant,
        "pair_id": variant_agg.variant_pair_id,
    }


# ── Human/LLM comparison ──────────────────────────────────────────────────────


def compare_human_llm_bsi(
    human_cell: HumanCellAggregate,
    llm_cell: "CellAggregate",
) -> HumanComparisonResult:
    """Compare human and LLM BSI for the same scenario cell.

    Implements the H10 test: independent two-sample comparison of
    ``mean_bsi(LLM, T=0.7, standard)`` versus ``mean_bsi(humans)``.

    Effect size (Cohen's d) is estimated using the pooled standard deviation:
    - Human variance: binomial ``p(1-p) / n`` (Wilson rate estimate)
    - LLM variance: empirical from ``std_bsi ** 2``

    Args:
        human_cell:  :class:`HumanCellAggregate` for the scenario variant.
        llm_cell:    :class:`~results.aggregate_cells.CellAggregate` for the
                     same scenario variant (same ``variant_pair_id`` and
                     ``variant``).

    Returns:
        :class:`HumanComparisonResult` with BSI difference, Cohen's d, and CI.
    """
    human_bsi = human_cell.mean_bsi
    llm_bsi = llm_cell.mean_bsi
    diff = human_bsi - llm_bsi

    n_human = human_cell.n_valid_subjects
    n_llm = llm_cell.n_valid_runs

    # Variance estimates
    p_human = human_cell.choice_rate_optimal
    var_human = p_human * (1.0 - p_human) / max(1, n_human)  # binomial variance of rate
    var_llm = (llm_cell.std_bsi ** 2)  # empirical variance of BSI

    pooled_std = math.sqrt(
        (max(1, n_human - 1) * var_human + max(1, n_llm - 1) * var_llm)
        / max(2, n_human + n_llm - 2)
    )
    cohens_d = diff / pooled_std if pooled_std > 0 else 0.0

    # 95 % CI on difference
    ci_lower, ci_upper = _difference_ci_95(diff, var_human, var_llm, n_human, n_llm)

    cell_id = f"{human_cell.variant_pair_id or human_cell.scenario_id}__{human_cell.variant}"

    return HumanComparisonResult(
        cell_id=cell_id,
        bias_category=human_cell.bias_category,
        variant=human_cell.variant,
        human_mean_bsi=round(human_bsi, 6),
        llm_mean_bsi=round(llm_bsi, 6),
        bsi_difference=round(diff, 6),
        cohens_d=round(cohens_d, 6),
        ci_lower_95=round(ci_lower, 6),
        ci_upper_95=round(ci_upper, 6),
        n_human=n_human,
        n_llm=n_llm,
    )


# ── I/O helpers ───────────────────────────────────────────────────────────────


def write_human_cell_report(
    report: HumanCellReport,
    output_dir: str | Path,
    filename: str = "human_cell_aggregates.json",
) -> Path:
    """Serialise *report* to ``{output_dir}/{filename}`` and return the path."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    out_path.write_text(report.model_dump_json(indent=2, exclude_none=False))
    return out_path


def write_human_comparisons(
    comparisons: list[HumanComparisonResult],
    output_dir: str | Path,
    filename: str = "human_llm_comparison.json",
) -> Path:
    """Serialise a list of :class:`HumanComparisonResult` to JSON."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    payload = [c.model_dump() for c in comparisons]
    out_path.write_text(json.dumps(payload, indent=2))
    return out_path
