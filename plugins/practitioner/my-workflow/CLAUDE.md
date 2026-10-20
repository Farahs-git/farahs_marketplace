# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this plugin.

## What This Plugin Is

A practitioner plugin for end-to-end domain object management in My Product. It automates the research, build, validate, and activate workflow.

## Repository Layout

- `skills/my-workflow/` -- The skill directory
- `skills/my-workflow/SKILL.md` -- Skill definition: YAML frontmatter (metadata) + Markdown body (system prompt)
- `skills/my-workflow/references/` -- Domain reference documents loaded on demand
- `skills/my-workflow/scripts/` -- Standalone Python CLIs that output JSON to stdout
- `skills/my-workflow/templates/` -- Domain object templates with placeholder values
- `skills/my-workflow/prompts/` -- LLM prompt templates for intent classification and generation
- `skills/my-workflow/evals/evals.json` -- Behavioral test cases
- `.claude-plugin/plugin.json` -- Claude Code plugin manifest
- `.mcp.json` -- MCP server configuration (optional)

## Script Conventions

- All scripts accept `--help` for usage information
- All scripts output JSON to stdout
- Success: `{"success": true, ...}`
- Failure: `{"success": false, "error": "..."}` with `sys.exit(1)`
- Single external dependency: `httpx>=0.27` (or `requests`)
- Environment variables for auth -- never hardcode credentials

## Environment Variables

### Required

- `MY_PRODUCT_BEARER_TOKEN` -- Valid bearer token
- `MY_PRODUCT_API_KEY` -- API key for your integration
- `MY_PRODUCT_BASE_URL` -- API base URL (e.g., `https://api.example.com`)

## Adding a New Skill

1. Create `skills/<skill-name>/` with `SKILL.md`, and optionally `scripts/`, `references/`, `templates/`, `prompts/`, `evals/evals.json`
2. Skill names use lowercase-hyphenated format
3. Update `../../.claude-plugin/marketplace.json` to register the new skill's parent plugin (if it is a new plugin)
