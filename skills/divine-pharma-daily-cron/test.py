
#!/usr/bin/env python3
"""Test script to verify divine-pharma-daily-cron skill can be loaded"""
import os
from pathlib import Path

skill_path = Path(__file__).parent / "SKILL.md"
if skill_path.exists():
    print("✓ Skill file exists")
    content = skill_path.read_text()
    if "name: divine-pharma-daily-cron" in content:
        print("✓ Skill name correct")
    else:
        print("✗ Skill name incorrect")
    print(f"✓ Skill content length: {len(content)} characters")
else:
    print("✗ Skill file missing")
