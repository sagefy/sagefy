---
title: Contributor Planning
layout: default
---

<style>img { max-width: 100% }</style>

At first, there will only be video information with multiple choice questions with textual questions, answers, and feedback. Later stages will add more formats.

Contributor Models
------------------

### Card

- id
- created
- modified
- language
- unit
- name (e.g. title)
- versioning (canonical)
- tags
- requires
- Videos
    - duration
    - url
- Text Multiple Choice Question
    - question
    - attempts allowed
    - max choices
    - multiple correct
    - answers
        - body
        - correct (boolean)
        - feedback

### Unit

- id
- created
- modified
- language
- versioning (canonical)
- name (title)
- body (objective, goal, description)
- requires

### Set

- id
- created
- modified
- language
- units
- sets
- name
- body (description, objective)
- versioning

### Discussion > Topic

- id
- created
- modified
- entity kind and id
- name

### Discussion > Post

- id
- created
- modified
- user
- topic
- body
- [kind]

### Discussion > Proposal

- Post +
- entity version
- action (create, update, delete ... split, merge)
- status (pending, blocked, accepted, declined)
- name

### Discussion > Vote

- Post +
- proposal
- kind (consent, discuss, dissent)

### Discussion > Flag

- Proposal +
- reason (offensive, irrelevant, incorrect, unpublished, duplicate, inaccessible)

Contributor Endpoints
---------------------

### Card, Unit, Set API

- GET `/cards/` (search)
- GET `/cards/{id}`
- GET `/units/` (search)
- GET `/units/{id}`
- GET `/sets/` (search)
- GET `/sets/{id}`

### Discussion API

- GET `/topics/` (search)
- POST `/topics/` (create topic)
- PUT `/topics/{id}` (update topic)
- GET `/topics/{id}/posts` (list posts)
- POST `/topics/{id}/posts` (create post, proposal, vote...)
- PUT `/topics/{id}/posts/{id}` (update post)

### Follow API

- POST `/follows/`
- DELETE `/follows/{id}`

Contributor Screen Requirements & Wireframes
--------------------------------------------

### Discussion

- cards in list
    - user avatar
    - username
    - date time
    - body
    - actions (edit, reply, vote, share, flag)
- infinite scroll with pagination
- reverse chronological
- proposal
    - list of proposal blocks and posts
        - Proposal block
            - proposal name
            - proposal body
            - proposal action
            - proposal decision
        - Posts
            - see below
    - Final block
        - Write post
        - Amend proposal (if owned)
        - Vote block (if not owned)
    - Considerations
        - [Contributor Ratings and Proposal Friction](/f_planning/contributor_ratings)

<img src="https://docs.google.com/drawings/d/1nIvhNcseLdUu4qzEN_0zfu9QenneynwFgmuDiZp5JC0/pub?w=913&amp;h=1136">

### Create Post or Vote

### Create Proposal

- language (create: select, edit: view)
- Preview edit/create
- Fields: see above
- **Create/Edit Card**
    - Kind selection changes fields available
- **Create/Edit Unit**
- **Create/Edit Set**

### Edit Post

### List, Search, Filter and Sort View (Template)

- Search box and button
- No results mode
- List
    - Infinite scroll
- Order by
- Filter by
    - Language
    - ...

<img src="https://docs.google.com/drawings/d/1U3EjKczxkUanbjwgLsk81oFJCcJsAMOIR7JJfBdVWxw/pub?w=1440&amp;h=1358">

#### Search Entities

- Search template + ...
- Order by
    - Latest
    - Watched
    - Proposals
    - Versions
    - Most connections
- Set
    - Show name, body (truncated), contains modules, components (truncated)
- Unit
    - Show name, kind, body (truncated), requires (truncated)
- Card
    - Video: show name, url (truncated), duration, tags (truncated)
    - Multiple choice text: show body (question, truncated)
- Show type (explode out card)

#### Search Topics and Discussion

- Search template + ...
- Topic name
- Number of posts
- Last modified

#### Search Versions

### View Entity (Template)

- Language
- Name
- Tags
- Flag
- Follow
- Contents (Changes by kind)
- Stats (Changes by kind)
    - Num Learners
    - See [Sequencer](/f_planning/sequencer)
- Relationships (Changes by kind)
- Topics
    - Topic name
    - Number of posts
    - Last modified
- Versions (joins with proposals)
    - Proposal name
    - Created
    - Proposal status (link to pr)

<img src="https://docs.google.com/drawings/d/1S8b5GQnZ2Wj7XPG0cYvS-ac_Syhx6Gcb5lq0gsYUbWk/pub?w=960&amp;h=1920">

#### View Card

- Template + ...
- Contents
    - Kind Specific Data
        - Video:
            - duration and url
        - Text Multiple Choice:
            - question
            - answers and feedback
            - options
- Relationships
    - Belongs to (unit)
    - Required By (card)
    - Requires (card)

#### View Unit

- Template + ...
- Contents
    - Body
- Stats
    - Number of cards > link to search
- Relationships
    - Requires (unit)
    - Required By (unit)
    - Belongs to (set)

#### View Set

- Template + ...
- Contents
    - Body
    - Members
- Stats
    - Number of units > link to search
- Relationships
    - Belongs to (set)

### What I'm Following

- Match search formatting
- Discussions
    - Topic name, modified, posts
    - My Proposals
        - Name, votes
- Link to search views
