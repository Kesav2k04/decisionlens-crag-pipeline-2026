# DecisionLens Documentation Quality Checklist

Use this checklist for README, demo script, project page, presentation notes, comments, and any public writing.

The goal is not to hide AI assistance. The goal is to produce accurate, specific, human-reviewed engineering communication.

## 1. Claim Integrity

Before publishing, every claim must have evidence.

Check each sentence that says the system can do something:

- Is it already implemented?
- Is there a test, screenshot, demo, or code path?
- Is the metric real?
- Is the source official?
- Is the limitation clear?

If not, rewrite it as pending, future work, or remove it.

Bad:

DecisionLens provides real-time VAR explanations for every World Cup match.

Better:

DecisionLens explains selected VAR-style incidents using retrieved rule evidence. Live match metadata is planned as a stretch feature.

## 2. Banned Or Risky Phrases

Avoid these unless there is a specific, proven reason:

- leveraging cutting-edge AI
- revolutionary
- game-changing
- seamless
- unlock insights
- harness the power
- state-of-the-art
- robust and scalable
- real-time, unless measured
- production-ready, unless deployed and tested
- 100 percent accurate
- fully automated trust
- replaces referees
- unbiased, unless evaluated
- industry-leading
- next-generation
- AI-powered platform, repeated everywhere

## 3. Preferred Style

Use:

- specific nouns.
- active verbs.
- short evidence-backed claims.
- clear limitations.
- examples from the actual prototype.
- exact tool roles.

Example:

DecisionLens parses official football rule documents with Docling, retrieves relevant rule sections, and asks Granite to explain the decision using only the retrieved evidence.

## 4. IBM Judge-Friendly README Structure

The final README should include:

1. Project title and one-sentence description.
2. Problem statement.
3. Why it matters for World Cup soccer.
4. Demo screenshot or short GIF.
5. How the system works.
6. IBM tools used and exact role of each.
7. Architecture diagram.
8. Setup instructions.
9. Example questions and outputs.
10. Evaluation method and results.
11. Limitations.
12. Future work.
13. Team and roles.

Do not bury the working demo below long background text.

## 5. IBM Tool Description Rules

For each IBM tool, answer:

- What did we use it for?
- Where is it in the code or workflow?
- Why was it needed?
- What evidence proves it works?

Bad:

We used IBM tools for advanced AI orchestration.

Better:

Docling converts IFAB rule PDFs into structured text chunks. Granite generates the final fan-facing explanation from retrieved chunks. LangFlow shows the retrieval-to-generation pipeline used in the demo.

## 6. Metrics Rules

Never publish placeholders like `[X]%` in final docs.

Allowed metrics:

- citation accuracy from deterministic tests.
- number of golden questions.
- retrieval top-k hit rate.
- RAGAS metrics if actually run.
- average local response time with machine details.
- token reduction if measured.

Every metric needs:

- command or script name.
- date measured.
- dataset size.
- machine/model details.
- result.

## 7. Limitations Section

Every serious README needs limitations.

Include:

- The system explains using available evidence; it does not replace officials.
- It cannot infer unseen video facts.
- Live VAR incident data may not be available.
- Confidence means evidence sufficiency, not guaranteed correctness.
- Official competition-specific rules must be verified.

This makes the project more credible, not weaker.

## 8. Repetition Check

Before finalizing, search for repeated words and phrases:

- AI-powered
- explainable
- transparent
- fans
- trust
- leverage
- insights
- real-time
- world-class
- innovative

If the same phrase appears too often, rewrite with more specific language.

## 9. Human Voice Check

A strong paragraph should sound like the team built and tested something.

Weak:

Our platform leverages artificial intelligence to provide seamless, transparent, and engaging football experiences.

Strong:

When a user asks why a goal was disallowed, DecisionLens retrieves the offside or handball rule sections, shows the source text, and explains which facts are still missing from the incident.

## 10. Demo Script Rules

The 3-minute demo should be tight:

0:00-0:25 - Problem: fans see a decision but not the reasoning.
0:25-1:25 - Live prototype: ask one decision question and show cited answer.
1:25-2:05 - Architecture: Docling, retrieval, Granite, UI.
2:05-2:35 - Evaluation: tests and citation checks.
2:35-3:00 - Impact and limitations.

Do not show long code walkthroughs in the demo video.

## 11. Project Page Rules

The project page should be shorter than README:

- one clear problem.
- one clear solution.
- IBM tools used.
- prototype link/repo.
- video.
- why it fits soccer and World Cup understanding.

Do not paste the whole README.

## 12. Final Review Checklist

Before submission, answer yes/no:

- Does the README match the actual prototype?
- Are all IBM tool claims true?
- Are all metrics real?
- Are all source citations accurate?
- Does the demo run without hidden manual steps?
- Does the project avoid score prediction and referee replacement?
- Does the text sound specific rather than generic?
- Did Codex review the README?
- Did Codex review the demo script?
- Did Codex review the project page text?
- Is the repo public?
- Is the project page published?

If any answer is no, fix before submitting.

