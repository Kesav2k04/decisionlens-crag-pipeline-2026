# langflow/decisionlens_component.py
# DecisionLens CRAG Agent — LangFlow Custom Component
# Wraps the real pipeline/agent.py run() so LangFlow orchestrates the
# actual hybrid retriever, CRAG evaluator, and Granite generation —
# not LangFlow's native vector/LLM components, which have no knowledge
# of the project's 532 Docling chunks or RRF fusion logic.

import os
import sys

from langflow.custom import CustomComponent


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
    icon = "⚽"

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
        # Resolve pipeline/ relative to this file so the component works
        # no matter which directory LangFlow was launched from.
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pipeline_dir = os.path.join(repo_root, "pipeline")
        if pipeline_dir not in sys.path:
            sys.path.insert(0, pipeline_dir)

        from agent import run

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
