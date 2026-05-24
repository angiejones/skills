---
name: recursive-code-review
description: Use this skill when reviewing uncommitted code changes, improving code quality before commit, or performing iterative feedback cycles on staged or unstaged diffs. Especially useful when the user wants deeper critique, multiple review passes, or systematic refinement before opening a PR.
metadata:
  author: angiejones
  version: "1.0"
---

# recursive-code-review

Use a dedicated review subagent to critique uncommitted code changes without modifying them directly. Apply the feedback, then repeat the review cycle with a new subagent until no meaningful issues remain or the review converges.

## When to use

Use this skill when reviewing staged or unstaged code changes before committing, improving implementation quality through iterative critique, or validating that recent edits do not introduce bugs, regressions, maintainability issues, or missing tests.

This skill is especially useful when:
- making non-trivial code changes
- refactoring existing code
- working across multiple files or services
- using AI-generated code
- preparing changes for commit or pull request
- validating fixes after addressing review feedback

## Instructions

1. Identify all staged and unstaged changes in the repository.

2. Generate a diff of the uncommitted changes to use as the review target.

3. Launch a dedicated review subagent with the following constraints:
   - The reviewer may analyze and critique the diff.
   - The reviewer must not modify files.
   - The reviewer should focus on correctness, regressions, maintainability, readability, test coverage, performance implications, security concerns, and risky patterns.
   - The reviewer should return actionable feedback with clear reasoning, severity, and file references.

4. Review the feedback and determine which issues should be addressed.

5. Apply fixes directly in the working tree.

6. After making changes, generate an updated diff and launch a new isolated review subagent with no memory of previous review passes.

7. Repeat the review and fix cycle until reviewers stop finding meaningful issues or feedback becomes repetitive and low value.

8. Before finishing, summarize:
   - Issues identified
   - Fixes applied
   - Remaining concerns, if any