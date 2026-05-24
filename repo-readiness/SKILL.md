---
name: repo-readiness
description: Use this skill when evaluating whether a repository is ready for AI-assisted development, improving how coding agents operate within a codebase, or identifying missing context and workflow documentation. Especially useful when the user wants better AI collaboration, more reliable agent behavior, or standardized AI workflows across a repository. Checks for agent context files, coding instructions, and reusable AI workflows, then recommends high-impact improvements and can help create missing artifacts on request.
metadata:
  author: angiejones
  version: "1.0"
---

# repo-readiness

Evaluate whether a repository is positioned for effective AI-assisted development by checking for signals that enable better AI collaboration.

## When to use

Use this skill when you need to:

- Assess a repository's readiness for AI-assisted development
- Check for agent context files, instruction files, and repeatable workflows
- Recommend improvements to make a repo more AI-friendly
- Help scaffold missing artifacts (AGENTS.md, copilot-instructions.md, SKILL.md, etc.)

## Overview

A repository "ready" for AI-assisted development has clear signals about:

1. **Agent context** — What agents and AI tools should know about this project
2. **Agent rules** — How AI should behave and what constraints apply
3. **Repeatable workflows** — Documented processes that can be automated or guided

This skill runs a deterministic evaluation script, interprets results, explains the score, and recommends the highest-impact improvements. If the user asks, you can help create the missing artifacts.

## Workflow

### Step 1: Run the evaluation script

Execute the evaluation script. With no argument, it evaluates the current directory. You can also pass a local path or GitHub `owner/repo` target.

```bash
python <skill-path>/scripts/evaluate_readiness.py
python <skill-path>/scripts/evaluate_readiness.py /path/to/local/repo
python <skill-path>/scripts/evaluate_readiness.py owner/repo
```

The script outputs JSON to stdout with:

- **score**: 0-100 readiness score
- **level**: "Not Ready", "Minimal", "Developing", "Advanced", or "Optimized"
- **signals_found**: Object with signal details for each category
- **recommendations**: Prioritized list of improvements (highest-impact first)
- **reasoning**: Explanation of the score

### Step 2: Format and explain the results

Display the results in a clear format:

1. Show the overall score and level
2. Display each scoring category as points earned out of the category maximum: Agent Context X/20, Agent Rules X/30, Repeatable Workflows X/30, Signal Maturity X/20
3. Display the signals that contributed to the score. Do not list missing interchangeable alternatives when another signal in that category already earned points.
4. For every category below its maximum score, inspect the contributing files before writing improvement guidance. Use the script output to identify the relevant files, then read those files and compare them to the scoring rules. Give one short, specific "How to improve" sentence that names the concrete missing or weak element. Do not give generic advice.
5. Present only the top recommendations in priority order. Keep this section concise: usually 2-3 items. Do not include low-impact improvements when larger scoring gaps remain. If the recommendations array is empty but the score is below 100, create concise recommendations from the lowest-scoring categories.

### Step 3: Recommend highest-impact improvements

When presenting recommendations, highlight:

- **Why** this would help AI-assisted development
- **What to do** to implement it
- **Impact** — how much this would improve the score

Do not stop at listing the score. If a category is below max, inspect the relevant files and explain the specific reason from the scoring rules. For example, if copilot-instructions.md lost points, say whether it lacks headings, rule/constraint language, or examples/code fences. For Signal Maturity, do not claim files are stale unless the script checks file age; explain the actual heuristic used by the script.

Prioritize by:

1. Foundational signals that enable other improvements (e.g., AGENTS.md before SKILL.md)
2. Frequency of use (e.g., copilot-instructions.md affects every AI interaction)
3. Ease of implementation

### Step 4: Help create missing artifacts (if requested)

If the user asks for help creating any of the missing artifacts, offer templates and guidance:

- **AGENTS.md**: Preferred high-level overview of this codebase for agents
- **CLAUDE.md**: Accepted fallback when AGENTS.md is not present
- **copilot-instructions.md**: Rules and constraints for AI (like .gitignore for AI)
- **SKILL.md files**: Repeatable workflows and expert patterns
- **prompts/**: Folder with reusable prompt templates

## Signals evaluated

The evaluation checks for these signals across the repository:

### Agent Context (20 points)

- `AGENTS.md` — Preferred project overview for agents
- `CLAUDE.md` — Fallback project overview when AGENTS.md is not present

If both files exist, evaluate AGENTS.md and ignore CLAUDE.md.

### Agent Rules (30 points)

These signals are interchangeable. Any one of the following can satisfy the Agent Rules category:

- `copilot-instructions.md` — AI behavior rules and constraints, found anywhere in the repository
- `prompts/` — Reusable prompt templates with at least one file

### Repeatable Workflows (30 points)

These signals are interchangeable. A repo can earn Repeatable Workflows points from either file type without needing both. The score is based on the stronger of the two counts.

- `SKILL.md` files — Documented expert patterns and workflows
- `recipe.yaml` files — Recipe-based workflow configuration

### Signal Maturity (20 points)

Signal Maturity is based on recognized signal coverage, not file age. The script counts whether the repo has agent context, agent rules, and repeatable workflow signals.

## Example output

```
READINESS EVALUATION RESULTS
════════════════════════════

Score: 62/100
Level: Developing ⚙️

Score Breakdown:
- Agent Context: 18/20
- Agent Rules: 30/30
- Repeatable Workflows: 8/30
- Signal Maturity: 10/20

Signals Found:
✓ AGENTS.md (18/20 pts)
✓ copilot-instructions.md (30/30 pts)
✓ src/utils/SKILL.md (8/30 pts)

How to improve:
1. Agent Context: Add more project-specific detail or structure to the selected context file to move from 18/20 to 20/20.
2. Repeatable Workflows: Add more SKILL.md or recipe.yaml workflows for recurring tasks; one workflow file earns partial credit.
3. Signal Maturity: Add whichever major signal category is missing; the maturity score is based on recognized signal coverage, not file age.
```

## Tips for implementation

- **Start with AGENTS.md**: It's the foundation. Everything else builds on it.
- **Review yearly**: Readiness can drift as the codebase evolves. Re-run annually.
- **Iterate**: Don't aim for 100. Focus on the top recommendations first.
- **Team feedback**: These signals are most valuable when the team maintains them together.
