---
name: skills-cli-guide
description: Use this skill when working with the Agent Skills CLI (npx skills), including installing, finding, updating, validating, uninstalling, troubleshooting, or documenting skills. Especially useful when the user needs correct command usage, help resolving CLI errors, or guidance managing skills locally.
license: Apache-2.0
compatibility: Requires Node.js/npm for npx skills commands; optional skills-ref validation for local skill package validation.
metadata:
  author: angiejones
  version: "1.0"
---

# skills-cli-guide

Use this skill whenever a task involves the Agent Skills CLI, installing a skill, writing install instructions, creating a skill package, updating a skill, removing a skill, or validating Agent Skills format.

The `skills` CLI is the primary way to install and manage skills for AI agents. The CLI can be run directly with `npx`; no installation is required:

Usage: `npx skills <command> [options]`

To get list of available commands and options, run:

```bash
npx skills --help
```

The CLI source code is available at https://github.com/vercel-labs/skills, and its [README.md](https://github.com/vercel-labs/skills/blob/main/README.md#skills) file lists all of the available commands and options with usage instructions. When unsure, consult the README.

Use the output from the CLI as the source of truth. 

## Installation Location

Global skills are installed under `.agents/skills/`, while local skills are installed in the current project directory. Use the `--global` or `-g` flag to specify global installation.

## Agent Skills Specification

There's a specification for how skills should be structured, including required files like `SKILL.md`. The CLI expects skills to follow this format for proper installation and management. Consult the [Agent Skills Specification](https://agentskills.io/specification) for details on how to structure a skill package.

## Validating skills

Use the [skills-ref reference library](https://github.com/agentskills/agentskills/tree/main/skills-ref) to validate a skills package.


```bash
git clone https://github.com/agentskills/agentskills.git
cd agentskills/skills-ref
uv run skills-ref validate /path/to/skill
```


This checks that a `SKILL.md` frontmatter is valid and follows all naming conventions.


