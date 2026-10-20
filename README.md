# My Team Extensions

AO (Agent Orchestrator) plugin extensions for My Team's product domain. Built on the [AO Harness](https://github.com/Adobe-Experience-Platform/agent-platform) plugin architecture.

> **New to AO?** Follow the [Getting Started guide](https://aep-ao.pages.adobeitc.com/) to set up your environment and learn how to develop plugin skills on AO.

## Quick Start

1. **Fork this template** and rename the repo to `<your-team>-extensions`
2. **Rename the example plugins** to match your domain (see [Customization](#customization) below)
3. **Add your skills** following the patterns in the example plugins
4. **Register skills** in a manifest to deploy them with the AO Harness

## Repository Layout

```
my-team-extensions/
  .claude-plugin/
    marketplace.json            # Master catalog of all plugins in this repo
  plugins/
    system/                     # Foundational service plugins (API docs, data access, shared tools)
      my-data-service/
        .claude-plugin/
          plugin.json           # Plugin manifest: name, description, version
        skills/
          my-data-service/
            SKILL.md            # Skill definition (YAML frontmatter + Markdown body)
            references/         # API docs and domain reference material
            evals/
              evals.json        # Behavioral test cases
    practitioner/               # Domain workflow plugins (multi-step processes, user-facing)
      my-workflow/
        .claude-plugin/
          plugin.json           # Plugin manifest with dependencies on system plugins
        skills/
          my-workflow/
            SKILL.md            # Skill definition
            references/         # Domain guides
            scripts/            # Python CLI tools (JSON output to stdout)
            templates/          # Domain object templates
            prompts/            # LLM prompt templates
            evals/
              evals.json        # Behavioral test cases
        .mcp.json               # Optional MCP server configuration
        CLAUDE.md               # Developer guidance for Claude Code
  docs/
    raw-requirements/           # PRDs, use cases, customer workflows
  tests/                        # End-to-end and integration tests
```

## Key Concepts

### Plugin Types

- **System plugins** provide foundational capabilities: API reference docs, data access layers, shared utilities. They are consumed by practitioner plugins via the `dependencies` field.
- **Practitioner plugins** implement domain workflows: multi-step processes that guide users through research, build, validate, and activate phases.

### Plugin Structure

Every plugin has:
- `.claude-plugin/plugin.json` -- Manifest with name, description, version, and optional dependencies
- `skills/<skill-name>/SKILL.md` -- The skill definition with YAML frontmatter (metadata) and Markdown body (system prompt and workflow)

A skill directory can optionally include:
- `references/` -- Domain docs, API specs, and guides the skill reads on demand
- `scripts/` -- Python CLI tools that output JSON to stdout
- `templates/` -- Domain object templates with placeholder values
- `prompts/` -- LLM prompt templates for sub-tasks
- `evals/evals.json` -- Behavioral test cases

### SKILL.md Frontmatter

```yaml
---
name: my-skill
description: |
  What: Brief description of what the skill does
  Why: Why it exists
  When: When to use it
metadata:
  version: "0.1.0"
  lifecycle: experimental
  dependencies:
    skills:
      - ref: other-skill
        required: true
apis:
  - service-name
databases:
  - db-name
---
```

- **lifecycle** must be `experimental` for all new skills. See the lifecycle policy below.
- **apis** lists the `api_request` service names the skill uses
- **databases** lists the `run_sql` database names the skill uses
- **dependencies.skills** declares skills this skill calls at runtime

### Evals

Every skill should have `evals/evals.json` with behavioral test cases:

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User input to test",
      "expected_output": "High-level expected behavior",
      "files": [],
      "expectations": [
        "The skill reads references/some-doc.md first",
        "The skill calls api_request with the correct parameters",
        "The skill presents results in a formatted table"
      ]
    }
  ]
}
```

Run evals using Claude Code's built-in skill evaluator:
```sh
/skill-creator run evals for my-skill
```

### Script Conventions

All Python scripts in `scripts/` must follow these conventions:
- Accept CLI arguments via `argparse` (support `--help`)
- Output JSON to stdout
- Return `{"success": true, ...}` on success
- Return `{"success": false, "error": "..."}` on failure with `sys.exit(1)`
- Never hardcode credentials -- use environment variables

## Installation

### Agent Platform

Add skill sources in your manifest YAML:

```yaml
skills:
  sources:
    - name: my-data-service
      source: path/to/my-team-extensions/plugins/system/my-data-service/skills/my-data-service
    - name: my-workflow
      source: path/to/my-team-extensions/plugins/practitioner/my-workflow/skills/my-workflow
```

### Claude Code

```sh
/plugin marketplace add my-org/my-team-extensions
/plugin install my-workflow@my-team-extensions
```

To auto-register for a project, add to `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "my-team-extensions": {
      "source": {
        "source": "github",
        "repo": "my-org/my-team-extensions"
      }
    }
  }
}
```

## Customization

When forking this template for your team:

1. **Rename the repo** to `<your-team>-extensions`
2. **Update `.claude-plugin/marketplace.json`**:
   - Change `name` to your repo name
   - Change `owner.name` to your team name
   - Replace the example plugins with your own
3. **Rename or replace the example plugins** under `plugins/system/` and `plugins/practitioner/`
4. **Update each `plugin.json`** with your plugin's name, description, and version
5. **Write your SKILL.md files** following the frontmatter format and workflow patterns shown in the examples

## Experimental Skills Policy

All new skills must include `lifecycle: experimental` in their SKILL.md frontmatter metadata.

Skills go through several iterations before being considered stable. The lifecycle metadata makes it easy for teams packaging agents to determine which skills are ready for different audiences (internal testing, early engagement, GA).

## Building Skills

Use Claude Code's built-in skill creator to author new skills:

```sh
/skill-creator
```

This walks you through creating a well-structured SKILL.md.

## Related

- [Agent Platform / AO Harness](https://github.com/Adobe-Experience-Platform/agent-platform) -- The AO Harness that runs agents
- [Claude Code Plugins](https://code.claude.com/docs/en/plugins) -- Plugin authoring guide
- [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) -- Marketplace specification
- [Discover Plugins](https://code.claude.com/docs/en/discover-plugins) -- How to find and install plugins
