---
name: my-workflow
description: >
  End-to-end workflow for creating and managing domain objects in My Product.
  What: Guides users through researching, building, validating, and activating
  domain objects.
  Why: Automates a multi-step process that requires coordination across
  several APIs and validation checkpoints.
  When: Use when the user wants to create, modify, or analyze domain objects.
metadata:
  version: "0.1.0"
  lifecycle: experimental
  dependencies:
    skills:
      - ref: my-data-service
        required: true
apis:
  - my-product
---

# My Workflow Skill

> **Tools available:** `api_request` (service="my-product") for API calls,
> `read`/`glob`/`grep` for exploring skill files. Scripts in `scripts/`
> are invoked via Bash and output JSON to stdout.

## Prerequisites

- Valid credentials available as environment variables
- Python 3.x runtime available
- The **my-data-service** system skill must be available for API reference

## Environment Configuration

```bash
export MY_PRODUCT_BEARER_TOKEN="your-token"    # Bearer token
export MY_PRODUCT_API_KEY="your-api-key"       # API key
export MY_PRODUCT_BASE_URL="https://api.example.com"  # API base URL
```

---

## Workflow Overview

| Phase | Step | Description | Implementation |
|-------|------|-------------|----------------|
| **RESEARCH** | 1 | Understand intent | Prompt 1 + domain-guide.md |
| **RESEARCH** | 2 | Discover existing objects | `scripts/example_query.py` |
| **BUILD** | 3 | Generate configuration | Templates + user input |
| **VALIDATE** | 4 | Preview and verify | API call via my-data-service |
| **ACTIVATE** | 5 | Create the object | API call via my-data-service |

---

## Phase 1: RESEARCH

### Step 1: Understand Intent

Read the domain guide to understand available object types and constraints:

```
read("references/domain-guide.md")
```

Classify the user's intent using the prompt template:

```
read("prompts/1-intent-classification.txt")
```

### Step 2: Discover Existing Objects

Run the discovery script to find objects matching the user's description:

```bash
python scripts/example_query.py --action search --query "user's search terms"
```

The script outputs JSON to stdout:
```json
{
  "success": true,
  "results": [...],
  "count": 5
}
```

---

## Phase 2: BUILD

### Step 3: Generate Configuration

Load the appropriate template:

```
read("templates/example-template.json")
```

Customize the template based on user input and the results from Step 2.

---

## Phase 3: VALIDATE

### Step 4: Preview and Verify

Present the generated configuration to the user for review. Validate it against the domain constraints from `references/domain-guide.md`.

---

## Phase 4: ACTIVATE

### Step 5: Create the Object

Use the **my-data-service** skill to identify the correct creation endpoint, then call the API:

```
api_request(
  service="my-product",
  path="/api/v1/items",
  method="POST",
  body={...}
)
```

---

## Error Handling

| Scenario | Handling |
|----------|----------|
| Script returns `success: false` | Report the `error` field to the user |
| API returns 401 | Credentials missing or expired -- inform the user |
| API returns 409 (conflict) | Object already exists -- ask user to rename or update |
| Validation failure | Present specific issues and ask user to correct |
