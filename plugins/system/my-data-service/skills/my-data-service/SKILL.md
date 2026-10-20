---
name: my-data-service
description: >
  API reference and documentation for My Product's data service. Provides
  endpoint documentation and API access via the api_request tool. Use this
  skill to look up endpoints, understand request/response schemas, or make
  API calls to the data service.
apis:
  - my-product
metadata:
  version: "0.1.0"
  lifecycle: experimental
---

# My Data Service

> **Tools available:** `api_request` for API calls, `read`/`glob`/`grep` for exploring docs.

## When to Use This Skill

**Use this skill when:**
- Looking up which API endpoint to use for a task
- Understanding request parameters, body schema, or response format
- Making direct API calls to the data service
- Referencing API conventions while working within a practitioner skill

**Do NOT use for:**
- Conceptual "what is" or "how does it work" questions
- Complex cross-entity analytical queries

## API Reference Structure

```
my-data-service/
├── SKILL.md
└── references/
    └── example-api/
        ├── _service.md       # Service overview and endpoint index
        └── list-items.md     # Per-endpoint documentation
```

## Endpoint Discovery Workflow

### Step 1: Identify the Service

Read the service overview to find the right endpoint:

```
read("references/example-api/_service.md")
```

### Step 2: Read Endpoint Documentation

Once you identify the endpoint, read its documentation:

```
read("references/example-api/list-items.md")
```

### Step 3: Make the API Call

```
api_request(
  service="my-product",
  path="/api/v1/items",
  method="GET"
)
```

The following headers are automatically injected -- do NOT include them:
`Authorization`, `Content-Type: application/json`, `Accept: application/json`

## Error Handling

| Scenario | Handling |
|----------|----------|
| 401 Unauthorized | Credentials missing or expired -- inform the user |
| 404 Not Found | Resource or endpoint does not exist |
| 500 Server Error | Report the error and suggest retrying |
