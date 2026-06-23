# langflow/decisionlens_component.py
# DecisionLens CRAG Agent — LangFlow Custom Component
# Wraps the real pipeline/agent.py run() so LangFlow orchestrates the
# actual hybrid retriever, CRAG evaluator, and Granite generation —
# not LangFlow's native vector/LLM components, which have no knowledge
# of the project's 593 Docling chunks or RRF fusion logic.

import importlib.util
import os
import sys
from pathlib import Path

from langflow.custom import CustomComponent

# Last-resort fallback when LangFlow UI paste runs outside the repo cwd
_DEFAULT_REPO = Path(r"D:\IBM SKILLS BUILD 2026 BEMYAPP\decisionlens-wc2026")


def _resolve_repo_root() -> Path:
    """Find DecisionLens repo root when loaded from file or LangFlow UI paste."""
    candidates: list[Path] = []

    env_root = os.environ.get("DECISIONLENS_ROOT")
    if env_root:
        candidates.append(Path(env_root).resolve())

    try:
        candidates.append(Path(__file__).resolve().parent.parent)
    except NameError:
        pass

    candidates.append(Path.cwd().resolve())
    candidates.extend(Path.cwd().resolve().parents[:5])
    candidates.append(_DEFAULT_REPO.resolve())

    seen: set[Path] = set()
    for root in candidates:
        if root in seen:
            continue
        seen.add(root)
        if (root / "pipeline" / "agent.py").is_file():
            return root

    raise RuntimeError(
        "DecisionLens repo not found. Set DECISIONLENS_ROOT to your repo folder "
        "(the one that contains pipeline/agent.py), then restart LangFlow."
    )


def _import_run():
    root = _resolve_repo_root()
    root_s = str(root)
    pipeline_s = str(root / "pipeline")
    for p in (root_s, pipeline_s):
        if p not in sys.path:
            sys.path.insert(0, p)

    try:
        from pipeline.agent import run

        return run
    except ModuleNotFoundError:
        agent_py = root / "pipeline" / "agent.py"
        spec = importlib.util.spec_from_file_location("decisionlens_agent", agent_py)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"Could not load {agent_py}") from None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.run


class DecisionLensCRAGAgent(CustomComponent):
    display_name = "DecisionLens CRAG Agent"
    description = (
        "Explains VAR and referee decisions from official IFAB rule text. "
        "Runs the full DecisionLens pipeline: hybrid BM25 + nomic-embed-text "
        "retrieval with RRF, CRAG evidence evaluation (GOOD >= 0.75 answers, "
        "POOR < 0.65 abstains), and IBM Granite 3.1 8B generation via Ollama. "
        "Requires Ollama running locally with granite3.1-dense:8b and "
        "nomic-embed-text pulled."
    )
    icon = "soccer"
    
    # Standardize all potential telemetry/tracking hooks expected by Langflow
    get_telemetry_input_values = lambda self: {}
    get_output_logs = lambda self: {}
    _token_usage = {}
    token_usage = {}

    def build_config(self) -> dict:
        return {
            "question": {
                "display_name": "Question",
                "info": (
                    "A football rule or VAR decision question, e.g. "
                    "'What makes a handball offence under FIFA Law 12?'"
                ),
                "multiline": True,
                "required": True,
            }
        }

    def build(self, question: str) -> str:
        run = _import_run()
        result = run(question)
        return self._format_markdown(result)

    @staticmethod
    def _format_markdown(result: dict) -> str:
        lines = []

        lines.append("## Explanation")
        lines.append(result.get("answer", "No answer generated."))
        lines.append("")

        confidence = result.get("confidence", 0.0)
        decision_type = result.get("decision_type", "unknown")
        lines.append(f"**Evidence confidence:** {confidence:.2f} "
                     "(evidence sufficiency, not factual certainty)")
        lines.append(f"**Decision type:** {decision_type.replace('_', ' ')}")
        lines.append("")

        steps = result.get("decision_steps", [])
        if steps:
            lines.append("### Decision steps")
            for i, step in enumerate(steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        citations = result.get("rule_citations", [])
        if citations:
            lines.append("### Rule citations")
            for c in citations:
                law = c.get("law_or_section", c.get("law", "Rule reference"))
                source = c.get("source", "IFAB rule documents")
                span = c.get("quoted_span", "")
                lines.append(f"- **{law}** — {source}")
                if span:
                    lines.append(f"  > \"{span}\"")
            lines.append("")

        missing = result.get("missing_evidence", [])
        if missing:
            lines.append("### Missing evidence")
            for item in missing:
                lines.append(f"- {item}")
            lines.append("")

        sources = result.get("sources", [])
        if sources:
            lines.append("### Sources")
            for s in sources:
                lines.append(f"- {s}")

        return "\n".join(lines)
