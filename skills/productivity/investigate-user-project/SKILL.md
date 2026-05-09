---
name: investigate-user-project
description: Systematic approach to exploring and understanding user projects or file systems when the exact structure is unknown
category: productivity
---

# Project Investigation Skill

## When to Use
When you need to explore and understand an existing user project, codebase, or file system to discover what's inside, especially when you don't know the exact structure or location.

## Why This Approach
Instead of guessing or making assumptions, this skill provides a systematic way to:
1. Search broadly then narrow down
2. Verify findings by examining actual file contents
3. Follow up on leads iteratively
4. Use a combination of built-in tools and custom scripts when needed

## Step-by-Step Process

### 1. Initial Broad Search
Start with general searches to get oriented:
- Search for keywords in file contents: `search_files(pattern="keyword", target="content")`
- Search for keywords in filenames: `search_files(pattern="keyword", target="files")`
- List directory contents to see what's available

### 2. Follow Up on Promising Leads
When you find potentially relevant files or directories:
- Read the actual file contents: `read_file(path="path/to/file")`
- Examine directory structure: Use `execute_code` with Python `pathlib` to explore
- Look for related files in the same area

### 3. Use Custom Search When Needed
If built-in search tools aren't sufficient, create a custom search script:
```python
import os
from pathlib import Path

# Example: Search for directories containing specific terms
home = Path.home()
found_paths = []
for root, dirs, files in os.walk(home):
    # Skip unproductive directories
    if any(skip in root for skip in ['.git', '__pycache__', 'node_modules', '.cache']):
        continue
        
    for dir_name in dirs:
        if any(term in dir_name.lower() for term in ['term1', 'term2']):
            full_path = Path(root) / dir_name
            found_paths.append(str(full_path.relative_to(home)))

# Report findings
```

### 4. Verify and Expand
For each promising lead:
- Check if it's a file or directory
- Read contents if it's a file
- List contents if it's a directory
- Look for related files nearby (same directory, parent directory, etc.)

### 5. Document What You Find
Keep track of:
- Files/directories found and their purposes
- Key contents discovered
- Gaps or things that weren't found
- Next steps if investigation needs to continue

## Tools to Use
- `search_files` - For finding files by name or content
- `read_file` - To examine file contents
- `execute_code` - For custom exploration scripts
- `terminal` - For shell commands like `ls`, `find`, `grep` when needed
- `patch`/`write_file` - If you need to create documentation of findings

## Verification Steps
Always verify by:
1. Checking file existence before reading
2. Confirming you're looking at the right file (path verification)
3. Reading actual contents rather than assuming based on name
4. Cross-referencing findings with multiple sources when possible

## Example Workflow
For investigating a project like "Devin's pharmacology project":
1. `search_files(pattern="pharmacology", target="content")`
2. `search_files(pattern="Devin", target="files")`  
3. If no direct hits, search home directory with custom script for variations
4. Examine any skill files or documentation found
5. Look for related directories mentioned in skills/documentation
6. Verify actual project structure vs. planned structure
7. Examine any reference materials or data files found

## Tips
- Start broad, then narrow based on findings
- Don't assume naming conventions - check variations
- Use context clues from file contents to guide next steps
- Remember that skills often document planned/intended structure, not necessarily current state
- Empty files or directories might indicate work-in-progress