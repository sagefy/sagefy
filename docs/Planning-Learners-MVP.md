---
layout: docs
title: Planning> Learners MVP
---

See [Sequencer](Planning-Sequencer), [Sequencer Background](Planning-Sequencer-Background) and [Machine Learning Requirements](Planning-Machine-Learning-Requirements).

Learner Models
--------------

**users_subjects**

- user_id : string
- subject_ids : array of strings

**responses**

- user_id : string
- card_id : string
- (unit_id : string) <- duplicate data, but convenient
- created : datetime
- score : number, 0 -> 1

**redis**

- user -> current subject
- user -> current unit
- caching

Learner Endpoints
-----------------

- GET `/s/users/{id}/subjects/`
- POST `/s/users/{id}/subjects/` <- Add to my subjects
- DELETE `/s/users/{id}/subjects/{id}` <- Remove from my subjects
- GET `/s/sequencer/next`
  - parameters: subject_id
  - returns: reference to one of the following endpoints
- GET `/s/subjects/{id}/tree` <- Show tree
  - returns: what would be the next action?
- GET `/s/subjects/{id}/units` <- Choose Unit screen
- PUT `/s/subjects/{id}/units/{id}` <- Unit chosen
- GET `/s/cards/{id}/learn` <- Render card
- POST `/s/cards/{id}/responses` <- Respond to card

Learner Screen Requirements and Wireframes
------------------------------------------

### My Subjects

<img src="https://docs.google.com/drawings/d/1jQFTFcNuIKIvsF3C9O4n2NkaRoxBVy0ZSE_ZtEVUb8Y/pub?w=1440&amp;h=1080">

### Search Subjects (...as learner)

<img src="https://docs.google.com/drawings/d/11xFDioVMAswGdr3CCIj2HqRiwy98NVUphO1MhzbAvoM/pub?w=1440&amp;h=1080">

### Tree

<img src="https://docs.google.com/drawings/d/1Q0ymTVBfv_GOk-qDwes0eks3BJGTC1O_p4z_Mq32xjw/pub?w=1440&amp;h=999">

### Choose Unit

<img src="https://docs.google.com/drawings/d/1DnXYfw5LkOdgdLeX1sB9UN1_pP8C81LHnS5g9s7nDL8/pub?w=1440&amp;h=1080">

### Card (...as learner)

<img src="https://docs.google.com/drawings/d/1d3ma1KBMXPLPyw2xtn0LiJerH4KqcNvQv2QVq3tmw2A/pub?w=1440&amp;h=1080">

#### Video Card

<img src="https://docs.google.com/drawings/d/14v8ShakN7Wij4n2L_7jFRrSHOllBpyowmdedLSi5JlE/pub?w=1440&amp;h=1080">

#### Choice Card

<img src="https://docs.google.com/drawings/d/1lKcNlQzstPCCf-n9rvDyTsz9oF1H8GLFsl-Yovnp9ns/pub?w=1440&amp;h=1080">
