# Example API Service

Base path: `/api/v1`

## Overview

The Example API provides CRUD operations for managing items in My Product.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/items` | List all items with optional filtering |
| GET | `/api/v1/items/{id}` | Get a single item by ID |
| POST | `/api/v1/items` | Create a new item |

## Authentication

All requests require a valid bearer token passed via the `Authorization` header (injected automatically by `api_request`).

## Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Maximum number of results (default: 20, max: 100) |
| `offset` | integer | Pagination offset |
| `orderBy` | string | Sort field (e.g., `created_at`, `name`) |
