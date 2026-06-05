---
name: notion-database-troubleshooting
description: Systematic approach to troubleshooting Notion database access issues
version: 1.0.0
author: Hermes Agent
category: productivity
---

# Notion Database Troubleshooting Skill

## When to Use This Skill
When you cannot access a Notion database using its known ID, or when database queries return 404 errors despite having valid API credentials.

## Common Causes
- Database was moved, deleted, or renamed
- Integration permissions were revoked or changed
- Database ID in configuration is outdated
- Database is in a workspace not shared with the integration
- Database was archived or moved to trash

## Step-by-Step Troubleshooting Process

### 1. Verify API Credentials
```bash
# Check that NOTION_API_KEY is set and valid
echo "NOTION_API_KEY length: ${#NOTION_API_KEY}"

# Test API connectivity with a simple search
curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
     -H "Notion-Version: 2022-06-28" \
     -d '{"page_size": 1}' \
     https://api.notion.com/v1/search
```

### 2. Search for Database by Name (if you know the approximate name)
```bash
# Replace with your search term
SEARCH_TERM="D.I. PHARM PODCASTS"

curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
     -H "Notion-Version: 2022-06-28" \
     -d "{\"query\": \"$SEARCH_TERM\", \"page_size\": 10}" \
     https://api.notion.com/v1/search
```

### 3. Search Specifically for Databases
```bash
# Replace with your search term
SEARCH_TERM="D.I. PHARM PODCASTS"

curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
     -H "Notion-Version: 2022-06-28" \
     -d "{\"query\": \"$SEARCH_TERM\", \"filter\": {\"value\": \"database\", \"property\": \"object\"}, \"page_size\": 10}" \
     https://api.notion.com/v1/search
```

### 4. List All Accessible Databases (if search doesn't work)
```bash
curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
     -H "Notion-Version: 2022-06-28" \
     -d '{"filter": {"value": "database", "property": "object"}, "page_size": 100}' \
     https://api.notion.com/v1/search
```

### 5. Check Database Sharing Settings
If you find the database in search results but still can't access it directly:
1. Verify the Notion integration is shared with the database
2. In Notion: Go to Database → ••• → Add connections → Check if your integration appears
3. The integration needs explicit permission to access each database

### 6. Look for Similar Database Names
Sometimes databases are renamed slightly:
- Check for variations in spacing, punctuation, or capitalization
- Look for similar names in your search results
- Common variations: "Divine Intervention Pharmacology", "DI Pharm Podcasts", etc.

### 7. Update Your Configuration
Once you find the correct database:
1. Note the new database ID from the search results
2. Update any skills, scripts, or configurations using the old ID
3. Test access with the new ID

## Verification Steps
After updating the database ID:
```bash
# Test direct access
curl -s -H "Authorization: Bearer $NOTION_API_KEY" \
     -H "Notion-Version: 2022-06-28" \
     -d '{"page_size": 1}' \
     https://api.notion.com/v1/databases/YOUR_DATABASE_ID/query

# Should return database metadata, not a 404 error
```

## Prevention Tips
1. Periodically verify critical database IDs still work
2. Consider storing database names alongside IDs for easier recovery
3. When setting up integrations, share all needed databases explicitly
4. Document database purpose and expected content for easier identification

## Example Workflow for Divine Intervention Pharmacology
Based on the session history:
1. The database was previously accessible at ID: `2f88c883-85ba-81ed-8d31-000b07f32c0e`
2. When that failed, searching for "D.I. PHARM PODCASTS" revealed related content
3. Searching specifically for databases with that term would have shown accessible databases
4. The correct approach is to update the skill/config with the newly discovered database ID

## Error Interpretation
- `404 object_not_found`: Database ID not found or not accessible to integration
- Check if database exists and integration has permission
- Verify the ID is correct (no typos/missing characters)