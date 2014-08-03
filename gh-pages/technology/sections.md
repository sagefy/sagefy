---
layout: default
title: Technology Sections
---

Sections
--------

- Core (API)
    - API core build first, separate from UIs
    - Database, Analysis
- Contribute UI
    - Interface for uploading content, practice, and designing application
    - Developing content relationships
    - Content feedback and peer review
- Learn UI
    - Primary learner interface
    - Learner data and progress
    - Most adaptive UI, language, technology, location...
- Analyze UI
    - Open anonymous statistics
    - Large-to-small picture
    - Useful for data scientists and educational scientists
    - Allows some querying
- Moderate UI
    - Additional interface for moderating discussion, content, conflicts
    - Promote conflict resolution strategies
    - Use democracy
- Mentor UI
    - Interface for learning by teaching
    - Answer learner questions on given topic
    - Suggest content changes by learner issues

Routing
-------

### ui/index.html

- `/`, `/login`, `/settings`, `/logout`, `/terms`, `/contact`
- `/learn`, `/learn/*`
- `/contribute`, `/contribute/*`
- `/analyze`, `/analyze/*`
- `/moderate`, `/moderate/*`
- `/mentor`, `/mentor/*`

### api/index.py

- `/api/*`

### External applications

- `/blog`, `/support`, `/questions`, `/feedback`
