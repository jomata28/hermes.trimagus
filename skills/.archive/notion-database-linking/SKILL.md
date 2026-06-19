---
name: notion-database-linking
description: Systematically link disconnected Notion databases that have relation fields but lack actual data connections. Use when databases are structured to be related but entries aren't actually linked, causing fragmentation in tracking systems.
version: 1.0.0
author: Hermes Agent + Community
license: MIT
prerequisites:
  env_vars: [NOTION_API_KEY]
  commands: [curl]
tags: [Notion, API, Database, Linking, Relations, Integration, Troubleshooting]
---
# Notion Database Linking Skill

This skill provides a systematic approach to link disconnected Notion databases that have relation fields defined but lack actual data connections between entries. Common when databases are set up to relate (e.g., Weekly Overview ↔ Workout Log) but the linking step requires manual intervention or was never implemented.

## When to Use This Skill

- You have Notion databases with relation fields that show 0 linked items despite having related data
- You've set up databases to track related information (weeks ↔ workouts, projects ↔ tasks, etc.) but they aren't actually connected
- You want to systematically link existing data based on matching criteria (dates, IDs, tags, etc.)
- Your Notion workspace feels fragmented because related data isn't visible together
- You've imported data or created entries without establishing the relations

## Step-by-Step Linking Process

### 1. Verify NOTION_API_KEY is Set Correctly

```bash
# Check what Hermes config shows
hermes config show | grep -A2 -B2 NOTION

# Check the actual .env file
cat ~/.hermes/.env | grep NOTION_API_KEY

# Extract the raw value
grep '^NOTION_API_KEY=REDACTED_IN_BACKUP
```

### 2. Identify the Databases to Link

Determine which databases need to be connected and understand their relationship:

```bash
# Get basic info about your databases
curl -s "https://api.notion.com/v1/databases/{DATABASE_ID}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"

# Remember: For API v2025-09-03+
# - Use database_id when creating pages or getting database info
# - Use data_source_id when querying (found in database info under data_sources array)
```

### 3. Discover Entry Structure and Matching Criteria

Analyze how entries in each database should be matched:

```bash
# Sample entries from first database
curl -s -X POST "https://api.notion.com/v1/data_sources/{DATA_SOURCE_ID_1}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 5}'

# Sample entries from second database  
curl -s -X POST "https://api.notion.com/v1/data_sources/{DATA_SOURCE_ID_2}/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 5}'
```

Look for matching fields like:
- Week numbers, dates, date ranges
- Project IDs, tags, categories
- Titles or names that correspond
- Custom relation properties

### 4. Develop Your Matching Strategy

Choose how to match entries between databases:

**Option A: Direct Field Match** (e.g., Week Number = Week Number)
**Option B: Date Range Match** (e.g., Workout Date falls within Week's Date Range)  
**Option C: ID or Reference Match** (e.g., explicit ID field)
**Option D: Hybrid Approach**

### 5. Create the Linking Script

Use this template to systematically link databases:

```python
import os
import json
import subprocess
import sys
from datetime import datetime, timedelta

# Get NOTION_API_KEY from environment
notion_key = os.getenv('NOTION_API_KEY')
if not notion_key:
    print("ERROR: NOTION_API_KEY not found in environment")
    sys.exit(1)

def notion_request(method, endpoint, data=None):
    """Make a request to Notion API"""
    url = f"https://api.notion.com/v1/{endpoint}"
    curl_cmd = [
        'curl', '-s',
        f'-X {method}',
        url,
        '-H', f'Authorization: Bearer {notion_key}',
        '-H', 'Notion-Version: 2025-09-03',
        '-H', 'Content-Type: application/json'
    ]
    
    if data is not None:
        curl_cmd.extend(['-d', json.dumps(data)])
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"API Error ({method} {endpoint}): {result.stderr}")
            return None
    except Exception as e:
        print(f"Request failed ({method} {endpoint}): {e}")
        return None

def get_all_pages(data_source_id, page_size=100):
    """Get all pages from a data source with pagination"""
    all_results = []
    has_more = True
    next_cursor = None
    
    while has_more:
        data = {"page_size": page_size}
        if next_cursor:
            data["start_cursor"] = next_cursor
            
        result = notion_request("POST", f"data_sources/{data_source_id}/query", data)
        if not result:
            break
            
        all_results.extend(result.get("results", []))
        has_more = result.get("has_more", False)
        next_cursor = result.get("next_cursor")
        
    return all_results

# CONFIGURE THESE FOR YOUR SPECIFIC USE CASE
# Database 1 (e.g., Weekly Overview)
DB1_ID = "your_first_database_id"
DB1_DS_ID = "your_first_data_source_id"
DB1_LINK_PROP = "Workout Log"  # Property name in DB1 that links to DB2

# Database 2 (e.g., Workout Log)  
DB2_ID = "your_second_database_id"
DB2_DS_ID = "your_second_data_source_id"
DB2_LINK_PROP = "Week Overview"  # Property name in DB2 that links to DB1

print(f"Loading data from both databases...")

# Get all entries
db1_entries = get_all_pages(DB1_DS_ID)
db2_entries = get_all_pages(DB2_DS_ID)

print(f"Found {len(db1_entries)} entries in Database 1")
print(f"Found {len(db2_entries)} entries in Database 2")

# Define your matching function
def should_link(db1_entry, db2_entry):
    """
    RETURN TRUE if these two entries should be linked
    CUSTOMIZE THIS BASED ON YOUR MATCHING CRITERIA
    """
    # Example: Match by week number
    db1_week = db1_entry.get('properties', {}).get('Week Number', {}).get('number')
    db2_week = db2_entry.get('properties', {}).get('Week Number', {}).get('number')
    if db1_week is not None and db2_week is not None:
        return db1_week == db2_week
    
    # Example: Match by date ranges
    # db1_date_range = db1_entry.get('properties', {}).get('Date Range', {}).get('date', {})
    # db2_date = db2_entry.get('properties', {}).get('Date', {}).get('date', {})
    # ... implement your date range logic ...
    
    return False  # Default: don't link

# Find and create links
links_created = 0
print("Searching for matches...")

for db1_entry in db1_entries:
    db1_id = db1_entry['id']
    matches = []
    
    for db2_entry in db2_entries:
        if should_link(db1_entry, db2_entry):
            matches.append(db2_entry['id'])
    
    if matches:
        # Link from DB1 to DB2
        relations = [{"id": mid} for mid in matches]
        result = notion_request("PATCH", f"pages/{db1_id}", {
            DB1_LINK_PROP: {"relation": relations}
        })
        if result:
            links_created += len(matches)
            print(f"  Linked DB1 entry to {len(matches)} DB2 entries")
        else:
            print(f"  FAILED to link DB1 entry")

# Optionally: Create reverse links (DB2 -> DB1)
print("\nCreating reverse links...")
reverse_links = 0
for db2_entry in db2_entries:
    db2_id = db2_entry['id']
    matches = []
    
    for db1_entry in db1_entries:
        if should_link(db1_entry, db2_entry):  # Same matching logic
            matches.append(db1_entry['id'])
    
    if matches:
        relations = [{"id": mid} for mid in matches]
        result = notion_request("PATCH", f"pages/{db2_id}", {
            DB2_LINK_PROP: {"relation": relations}
        })
        if result:
            reverse_links += len(matches)
            print(f"  Linked DB2 entry to {len(matches)} DB1 entries")
        else:
            print(f"  FAILED to link DB2 entry")

print(f"\n=== SUMMARY ===")
print(f"Created {links_created} forward links (DB1 → DB2)")
print(f"Created {reverse_links} reverse links (DB2 → DB1)")
```

### 6. Execute the Linking Process

Save the script above as `link_notion_dbs.py` and run it:

```bash
python link_notion_dbs.py
```

### 7. Verify the Links Worked

Check a few entries in each database to confirm the relations are now populated:

```bash
# Check a Database 1 entry
curl -s "https://api.notion.com/v1/pages/{PAGE_ID_FROM_DB1}" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03"

# Look for the relation property - it should now show linked items
```

## Common Matching Strategies

### Strategy 1: Week Number Matching (Fitness Tracking)
- **Database 1**: Weekly Overview (has Week Number)
- **Database 2**: Workout Log (has Week Number)
- **Match**: Where Week Number equals Week Number

### Strategy 2: Date Range Matching (Project Sprints)  
- **Database 1**: Sprints (has Start Date, End Date)
- **Database 2**: Tasks (has Due Date)
- **Match**: Where Task Due Date falls between Sprint Start and End Dates

### Strategy 3: Project/Category Matching
- **Database 1**: Projects (has Project Name/ID)
- **Database 2**: Tasks (has Project Relation or Project Name field)
- **Match**: Where Project identifiers match

### Strategy 4: Date-to-Date Matching (Daily Logging)
- **Database 1**: Daily Log (has Date)
- **Database 2**: Habits/Metrics (has Date)
- **Match**: Where Date equals Date

## Automation & Maintenance

### Create Database Templates
Once linked, create templates that automatically set up connections:

**For Weekly Overview Template:**
- Pre-set: [Leave Week Number blank for manual entry]
- Add reminder: "Remember to link workouts from this week using the linking script or manual linking"

**For Workout Log Template:**
- Pre-set: Date = @Today
- Pre-set: Session = [AM/PM based on time]
- **Crucial**: Add a step in your workflow to link to current week after creating

### Set Up Regular Maintenance
If you frequently add new entries:

1. **Weekly**: Run the linking script every Sunday to link new week's workouts
2. **After Import**: Run after importing data from other sources
3. **Before Reporting**: Run before generating views or dashboards that need linked data

## Troubleshooting

### "No matches found" 
- Double-check your matching criteria in the `should_link` function
- Verify date formats are consistent (ISO 8601: YYYY-MM-DD)
- Check that field names and property types are correct
- Test with a small sample first

### Links not showing in Notion UI
- Give it a few seconds - Notion sometimes takes time to update linked views
- Make sure you're looking at the correct relation property
- Try refreshing the page

### API rate limits
- Notion allows ~3 requests/second average
- The script above includes built-in delays via subprocess timeouts
- If you get rate limit errors, add `time.sleep(0.5)` between requests in the loop

## Using Within Hermes

You can execute this approach directly in Hermes using the `execute_code` tool:

1. Copy the Python script above
2. Wrap it in proper Python syntax if needed
3. Execute via `execute_code` tool
4. Monitor output for success/failure messages

## Verification Checklist

After linking, verify:
- [ ] Database 1 entries show linked items in Database 2 relation field
- [ ] Database 2 entries show linked items in Database 1 relation field  
- [ ] Linked databases views show related data together
- [ ] Rollup/formula properties now calculate correctly (if applicable)
- [ ] Your workflow feels less fragmented

## Example: Linking Fitness Tracking Databases

For a setup like:
- **Weekly Overview** (database) ↔ **Workout Log** (database)
- Match by: Week Number
- Link properties: "Workout Log" (in Weekly Overview) ↔ "Week Overview" (in Workout Log)

The skill would systematically:
1. Find all weeks and all workouts
2. Match entries where Week Numbers are equal
3. Create the bidirectional links
4. Allow you to see all week's workouts when viewing the weekly overview