---
name: notion-debug-and-query
description: Debug and troubleshoot Notion API integration in Hermes, then query project databases
version: 1.0.0
author: REDACTED
license: MIT
prerequisites:
  env_vars: [NOTION_API_KEY]
  commands: [curl, jq]
tags: [Notion, API, Debugging, Integration, Troubleshooting]
---

# Notion API Debugging and Querying Skill

This skill provides a systematic approach to troubleshooting Notion API integration issues in Hermes and querying project/workspace data.

## When to Use This Skill

- You're having trouble connecting to your Notion workspace through Hermes
- Need to verify your Notion API key is correctly configured
- Want to explore what's available in your Notion workspace
- Need to query a specific database (like a projects database)
- Encountering "API token is invalid" or unauthorized errors

## Step-by-Step Debugging Process

### 1. Verify NOTION_API_KEY is Set Correctly

```bash
# Check what Hermes config shows
hermes config show | grep -A2 -B2 NOTION

# Check the actual .env file
cat ~/.hermes/.env | grep NOTION_API_KEY

# Extract the raw value (important: hermes config may show masked values)
grep '^NOTION_API_KEY=' ~/.hermes/.env | cut -d'=' -f2
```

### 2. Test Both API Keys (if you have multiple)

If you've been provided multiple potential API keys, test them systematically:

```bash
# Test Key 1
KEY1="REDACTED"
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $KEY1" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "", "page_size": 1}'

# Test Key 2  
KEY2="REDACTED"
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $KEY2" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "", "page_size": 1}'
```

### 3. Set the Correct Key in Environment

Once you've identified the working key:

```bash
# Set it for current session
export NOTION_API_KEY="your_working_key_here"

# Or update it permanently in Hermes
hermes config set NOTION_API_KEY "your_working_key_here"
```

### 4. Verify Connection Works

```bash
# Simple search test
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "", "page_size": 5}' | jq '.'

# Should return successful JSON with results array
```

### 5. Discover What's in Your Workspace

```bash
# Get overview of your workspace
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "",
    "page_size": 100,
    "sort": {
      "direction": "descending",
      "timestamp": "last_edited_time"
    }
  }' | jq '.results | length, .[0:5] | {object, id, title}'
```

### 6. Find Your Projects Database

Search for databases related to projects:

```bash
# Search for project-related content
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "project", "page_size": 50}' | jq '.results[] | select(.object == "data_source") | {id, title}'
```

### 7. Query a Specific Database (Projects Example)

Once you have your projects database ID:

```bash
# Replace with your actual database ID
DATABASE_ID="52a1208a-b874-4d79-afdc-b574126454b5"

curl -s -X POST "https://api.notion.com/v1/data_sources/$DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "page_size": 50,
    "sorts": [{
      "timestamp": "last_edited_time",
      "direction": "descending"
    }]
  }' | jq '.results[] | {
    id: .id,
    name: .properties.Name.title[0].plain_text // .properties."Project Name".rich_text[0].plain_text // "Unnamed",
    status: .properties.Status.select.name // .properties.State.select.name // "No status",
    priority: .properties.Priority.select.name // .properties.Importance.select.name // "No priority"
  }'
```

### 8. Common Property Extraction Patterns

When querying databases, use these patterns to extract data:

- **Title**: `.properties.Name.title[0].plain_text`
- **Rich Text**: `.properties.Description.rich_text[0].plain_text`  
- **Select**: `.properties.Status.select.name`
- **Multi-select**: `.properties.Tags.multi_select[].name`
- **Date**: `.properties.DueDate.date.start`
- **Checkbox**: `.properties.Done.checkbox`
- **Number**: `.properties.Estimate.number`
- **URL**: `.properties.Link.url`

## Troubleshooting Tips

### "API token is invalid" Errors:
1. Double-check you're not accidentally logging the key somewhere
2. Verify the key starts with `secret_` or `ntn_`
3. Ensure you haven't accidentally included whitespace or newlines
4. Try regenerating the key in Notion integrations settings
5. Make sure you've shared target pages/databases with the integration

### Permission Errors:
1. In Notion, go to the page/database you want to access
2. Click "..." → "Connect to" → select your integration
3. The integration must be explicitly granted access to each piece of content

### API Version Issues:
- Always include `Notion-Version: 2025-09-03` header
- Use `/data_sources/` endpoints for queries (not `/databases/`)
- Remember: `database_id` for creating pages, `data_source_id` for querying

## Verification Steps

After setting up, verify with:
```bash
# Should return your workspace info without errors
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"
```

## Notes

- Page/database IDs work with or without dashes
- Rate limit: ~3 requests/second average
- Use `jq` for clean JSON output in terminal
- The `-s` flag in curl suppresses progress bars for cleaner output
- When in doubt, start with a broad search to see what's accessible
- **Important API v2025-09-03 specifics:**
  - Databases are called "data sources" in the API
  - Each database has TWO IDs:
    - `database_id`: Use when creating pages (`parent: {"database_id": "..."}`)
    - `data_source_id`: Use when querying (`POST /v1/data_sources/{id}/query`)
  - Search results return data sources with their `data_source_id`
  - Always include `Notion-Version: 2025-09-03` header

## Using execute_code for Notion API (when no direct tool exists)

When Hermes doesn't have a direct Notion tool but you have the notion skill, you can use execute_code to make API calls directly:

```python
import os
import json
import subprocess
import sys

notion_key = os.getenv('NOTION_API_KEY')
if not notion_key:
    print("ERROR: NOTION_API_KEY not found")
    sys.exit(1)

# Example: Search for pages
curl_cmd = [
    'curl', '-s', '-X', 'POST',
    'https://api.notion.com/v1/search',
    '-H', f'Authorization: Bearer {notion_key}',
    '-H', 'Notion-Version: 2025-09-03',
    '-H', 'Content-Type: application/json',
    '-d', '{"query": "", "page_size": 10}'
]

result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
if result.returncode == 0:
    data = json.loads(result.stdout)
    # Process results...

This skill saves the troubleshooting methodology learned when integrating Notion with Hermes, particularly focusing on credential verification, API testing, and systematic debugging of connection issues.