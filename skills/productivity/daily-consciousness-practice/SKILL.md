---
name: daily-consciousness-practice
description: System for delivering daily motivational/practice messages based on consciousness levels, values, and wisdom from historical figures
category: productivity
---

# Daily Consciousness Practice System

A system for delivering daily motivational/practice messages based on consciousness levels, values, and wisdom from historical figures.

## When to Use

Use this skill when you want to:
- Establish a daily practice for personal growth or consciousness raising
- Receive structured morning messages with specific values to embody
- Learn from wisdom of historical figures through daily spotlights
- Track your practice and reflections over time
- Integrate with Telegram for delivery and optionally Obsidian for knowledge building

## Prerequisites

- Hermes agent with cron job capability
- Telegram access (for message delivery)
- Optional: Obsidian vault (for knowledge integration)
- Optional: Google Drive or other storage (for source materials)

## Setup Instructions

### 1. Prepare Content Lists
Create and organize your reference materials:

```
300-Vibes/
├── 📄 values.txt          # One value per line (Kind, Warm, Diligent, etc.)
├── 📄 individuals.txt     # One individual per line (Aristotle, Bruce Lee, etc.)
├── 📄 teachings/          # Folder with teaching snippets
│   ├── aristotle.md
│   ├── brucelee.md
│   └── ...
├── 📄 practices/          # Folder with practice suggestions
│   ├── kind.md
│   ├── diligent.md
│   └── ...
└── 📄 reflections/        # Folder with reflection prompts
    ├── kind.md
    ├── diligent.md
    └── ...
```

### 2. Create the Message Template
Define your daily message structure:

```
🌅 300 VIBES MORNING - [Date]

VALUE OF THE DAY: [VALUE]
> [Brief explanation of what this value means in practice]

TEACHER SPOTLIGHT: [INDIVIDUAL]
> [Relevant quote or teaching snippet]

TODAY'S PRACTICE: [SPECIFIC ACTION]
> [Clear, actionable habit for the day]

REFLECTION: [QUESTION]
> [Evening reflection question]
```

### 3. Set Up the Cron Job
Use Hermes to create a scheduled job:

```bash
# In Telegram with Hermes:
/cronjob add 300-vibes "Send daily 300 vibes message" "55 13 * * *" "python3 -c "
import datetime
import random

# Load your content files (adjust paths as needed)
with open('values.txt') as f:
    values = [line.strip() for line in f if line.strip()]
with open('individuals.txt') as f:
    individuals = [line.strip() for line in f if line.strip()]

# Select today's elements
today = datetime.date.today()
random.seed(today.toordinal())  # Consistent but rotating selection
value = random.choice(values)
individual = random.choice(individuals)

# Load corresponding teaching, practice, reflection
# (Implement file loading logic here)

message = f"""🌅 300 VIBES MORNING - {today}

VALUE OF THE DAY: {value}
> [Explanation]

TEACHER SPOTLIGHT: {individual}
> [Quote]

TODAY'S PRACTICE: [Action]
> [Description]

REFLECTION: [Question]
> [Prompt]"""

print(message)"
```

### 4. Optional: Obsidian Integration
For deeper knowledge integration:

1. Create a "300-Vibes" folder in your Obsidian vault
2. Create templates for:
   - Daily notes (auto-populated with value/individual)
   - Value reference notes
   - Individual reference notes
   - Practice logs
3. Use Templater or Dataview plugins to:
   - Auto-select value/individual of the day
   - Log your practice reflections
   - Generate weekly/monthly reports

### 5. Customization Options
- **Frequency**: Adjust cron schedule (daily, weekdays only, etc.)
- **Delivery**: Change recipient (group, DM, email)
- **Content Source**: Use Google Drive, Notion, or local files
- **Selection Algorithm**: Random, sequential, need-based, etc.
- **Format**: Adjust length, tone, emoji use, etc.

## Troubleshooting

- **Messages not sending**: Check cron job status with `/cronjob list`
- **Content loading errors**: Verify file paths and permissions
- **Format issues**: Test message generation manually before scheduling
- **Timezone confusion**: Remember Hermes uses UTC internally (CT = UTC-5/-6)

## Tips for Success

1. Start simple - get the basic message working first
2. Rotate content systematically to ensure coverage
3. Keep practices specific and actionable (avoid vague advice)
4. Make reflection questions open-ended and personal
5. Review monthly to see which values/practices resonated most
6. Consider adding voice note options for variety
7. Allow occasional "free choice" days based on intuition

## Related Skills
- `obsidian` - For knowledge base integration
- `google-workspace` - For Drive/Calendar integration
- `telegram` - For messaging platform specifics
- `investigate-user-project` - For exploring your existing systems

This system combines timeless wisdom with modern habit formation to create a practical path for consciousness growth and value embodiment.