---
name: notion-active-projects-query
description: Query Notion for active projects with systematic troubleshooting and property extraction patterns
version: 1.0.0
author: community
license: MIT
tags: [Notion, API, Projects, Query, Troubleshooting]
prerequisites:
  env_vars: [NOTION_API_KEY]
  commands: [curl, jq]
---

# Notion Active Projects Query Skill

This skill provides a reliable method to query your Notion workspace for active projects, incorporating lessons learned from troubleshooting common issues like incorrect property values, case sensitivity, and API version specifics.

## When to Use This Skill

- You need to list all active projects from your Notion projects database
- You're troubleshooting Notion API connection issues
- You want to extract specific project properties (name, status, dates, etc.)
- You've encountered "select option not found" errors when querying

## Step-by-Step Process

### 1. Verify NOTION_API_KEY Configuration

```bash
# Check the actual .env file (Hermes config may show masked values)
grep '^NOTION_API_KEY=' ~/.hermes/.env | cut -d'=' -f2

# Test the key with a simple API call
curl -s -X POST "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

### 2. Test Your Projects Database Connection

Replace `YOUR_DATABASE_ID` with your actual projects database ID:

```bash
# Test basic connectivity to the database
curl -s -X POST "https://api.notion.com/v1/data_sources/YOUR_DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 1}'
```

### 3. Discover Actual Status Property Values

If you get "select option not found" errors, first check what values actually exist:

```bash
# Get a sample of items to see what Status values are used
curl -s -X POST "https://api.notion.com/v1/data_sources/YOUR_DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 5}' | jq '.results[0].properties.Status'
```

**Common Status values we encountered:**
- `"ACTIVE"` (uppercase)
- `"PLAN"` (uppercase)
- `"REVIEW"` (uppercase)
- `"SLEEP"` (uppercase)
- `"Planned"` (capitalized)
- `"Done"` (capitalized)

### 4. Query for Active Projects

Once you know the correct Status value for "active" (likely `"ACTIVE"`):

```bash
DATABASE_ID="52a1208a-b874-4d79-afdc-b574126454b5"  # Your projects database ID

curl -s -X POST "https://api.notion.com/v1/data_sources/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "property": "Status",
      "select": {
        "equals": "ACTIVE"  # Use the actual value from step 3
      }
    },
    "sorts": [
      {
        "property": "Date",
        "direction": "descending"
      }
    ],
    "page_size": 100
  }' | jq -r '.results[] | 
    "\(.id) | \(.properties.Name.title[0].plain_text // "Untitled") | Status: \(.properties.Status.select.name // "No Status") | Date: \(.properties.Date.date.start // "No Date")"
  '
```

### 5. Extract Common Project Properties

Use these jq patterns to extract data from Notion database items:

- **Project Name**: `.properties.Name.title[0].plain_text`
- **Status**: `.properties.Status.select.name`
- **Start Date**: `.properties.Date.date.start`
- **End Date**: `.properties.Date.date.end` (if applicable)
- **Relation field** (e.g., Related People): `.properties.RelatedPeople.relation[].id`
- **Rich text** (e.g., Description): `.properties.Description.rich_text[0].plain_text`
- **Number**: `.properties.Estimate.number`
- **URL**: `.properties.Link.url`
- **Checkbox**: `.properties.Done.checkbox`

## Troubleshooting Tips from Experience

### "select option \\\"Active\\\" not found" Errors
1. **Check case sensitivity**: Notion API v2025-09-03 is case-sensitive for select options
2. **Verify actual values**: Query a few items first to see what values are actually stored
3. **Look for variations**: We found "ACTIVE" (uppercase) worked, not "Active" or "active"
4. **Check for similar options**: Sometimes there are multiple similar options like "PLAN" vs "Planned"

### API Version Specifics (v2025-09-03)
- Always use `Notion-Version: 2025-09-03` header
- Use `/data_sources/` endpoint for querying (not `/databases/`)
- Remember: Each database has TWO IDs:
  - `database_id`: Use when creating pages (`parent: {"database_id": "..."}`)
  - `data_source_id`: Use when querying (`POST /v1/data_sources/{id}/query`)
- In search results, the `id` field is the `data_source_id`

### Permission Issues
- Ensure your Notion integration is connected to the target database
- In Notion: Open database → "..." → "Connect to" → select your integration
- Without explicit connection, you'll get 404 or permission errors

## Using with execute_code (Python)

When you need more complex processing, wrap the API calls in Python:

```python
import os
import json
import subprocess

def query_notion_active_projects(database_id):
    notion_key = os.getenv('NOTION_API_KEY')
    if not notion_key:
        raise ValueError("NOTION_API_KEY not found in environment")
    
    curl_cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://api.notion.com/v1/data_sources/{database_id}/query',
        '-H', f'Authorization: Bearer {notion_key}',
        '-H', 'Notion-Version: 2025-09-03',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({
            "filter": {
                "property": "Status",
                "select": {"equals": "ACTIVE"}
            },
            "sorts": [{"property": "Date", "direction": "descending"}],
            "page_size": 100
        })
    ]
    
    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Curl failed: {result.stderr}")
    
    data = json.loads(result.stdout)
    if 'results' not in data:
        raise ValueError(f"Unexpected response: {data}")
    
    projects = []
    for page in data['results']:
        props = page['properties']
        project = {
            'id': page['id'],
            'name': props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Untitled'),
            'status': props.get('Status', {}).get('select', {}).get('name', 'No Status'),
            'start_date': props.get('Date', {}).get('date', {}).get('start'),
            'end_date': props.get('Date', {}).get('date', {}).get('end')
        }
        projects.append(project)
    
    return projects

# Usage
if __name__ == "__main__":
    projects = query_notion_active_projects("52a1208a-b874-4d79-afdc-b574126454b5")
    for p in projects:
        print(f"{p['name']} - {p['status']} - {p['start_date']}")
```

## Verification

After querying, verify results make sense:
- Check that all returned items actually have Status: ACTIVE
- Look for unexpected duplicates or missing projects
- Verify date formats are consistent (YYYY-MM-DD)

This skill captures the systematic approach we developed to reliably query active projects from Notion, including handling the specific quirks of the Notion API v2025-09-03 and troubleshooting common authentication and property value issues.