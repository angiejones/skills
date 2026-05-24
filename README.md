Library of Agent Skills I've developed and use.

## Recursive Code Review

Adversarial subagent code review skill that teaches how to review uncommitted changes before they’re finalized by creating a separation between the "builder" and the "reviewer." Instead of letting the main agent judge its own work, it delegates review to a separate subagent whose job is to critique the diff. This review-fix cycle continues until reviewers stop finding meaningful issues.

Install:

```
npx skills add angiejones/skills --skill recursive-code-review -g
```


## Repo Readiness

Evaluate whether a repository is positioned for effective AI-assisted development by checking for signals that enable better AI collaboration.

Install:

```
npx skills add angiejones/skills --skill repo-readiness -g
```

## Skills CLI Guide

My agent always acts clueless when I try to get it to use the Skills CLI. This skill provides some documentation to help guide the agent.

Install:

```
npx skills add angiejones/skills --skill skills-cli-guide -g
```


