---
title: Learners (MVP) Requirements
layout: default
---

See [Sequencer](/f_planning/sequencer), [Sequencer Background](/f_planning/sequencer_background) and [Machine Learning Requirements](/f_planning/ml_requirements).

Learner Models
--------------

**users_sets**

- user_id : string
- set_ids : array of strings

**responses**

- user_id : string
- card_id : string
- (unit_id : string) <- duplicate data, but convenient
- created : datetime
- score : number, 0 -> 1

**redis**

- user -> current set
- user -> current unit
- caching

Learner Endpoints
-----------------

- GET `/s/users/{id}/sets/`
- POST `/s/users/{id}/sets/` <- Add to my sets
- DELETE `/s/users/{id}/sets/{id}` <- Remove from my sets
- GET `/s/sequencer/next`
    - parameters: set_id
    - returns: reference to one of the following endpoints
- GET `/s/sets/{id}/tree` <- Show tree
    - returns: what would be the next action?
- GET `/s/sets/{id}/units` <- Choose Unit screen
- PUT `/s/sets/{id}/units/{id}` <- Unit chosen
- GET `/s/cards/{id}/learn` <- Render card
- POST `/s/cards/{id}/responses` <- Respond to card

Learner Screen Requirements and Wireframes
------------------------------------------

### My Sets

<img src="https://docs.google.com/drawings/d/1jQFTFcNuIKIvsF3C9O4n2NkaRoxBVy0ZSE_ZtEVUb8Y/pub?w=1440&amp;h=1080">

### Search Sets (...as learner)

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
