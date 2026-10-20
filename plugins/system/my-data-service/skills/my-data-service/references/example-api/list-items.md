# List Items

**Method:** `GET`
**Path:** `/api/v1/items`
**Service:** `my-product`

## Description

Returns a paginated list of items. Supports filtering by status and name.

## Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | integer | No | Max results per page (default: 20) |
| `offset` | integer | No | Pagination offset (default: 0) |
| `status` | string | No | Filter by status: `active`, `archived`, `draft` |
| `name` | string | No | Filter by name (case-insensitive substring match) |

## Example Request

```
api_request(
  service="my-product",
  path="/api/v1/items?limit=10&status=active",
  method="GET"
)
```

## Example Response

```json
{
  "items": [
    {
      "id": "item-001",
      "name": "Example Item",
      "status": "active",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total_count": 42,
  "limit": 10,
  "offset": 0
}
```
