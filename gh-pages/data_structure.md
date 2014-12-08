---
title: Data Structure
layout: default
---

This document covers the overall architecture of Sagefy's data storage. This data structure allows Sagefy to be both open-content as well as highly adaptive and flexible while maintaining practicality.

![Data Structure Example: Statistics](https://docs.google.com/drawings/d/1idC1i8udNsD5C1yj1K7qKp6cwSkyhwjLXzG-xsXG6gE/pub?w=735&amp;h=280)

Cards
-----

Cards are the smallest entity in the Sagefy data structure system. A card represents a single learner activity.

A card could present information, ask the learner to answer a question, collaborate with a small group to tackle a challenge, or create other cards.

### Card Kinds

Some kinds may include a video, a multiple choice question, or interactive demonstration. For more, see [Data Structure: Card Kinds](/f_data_structure/cards).

### Card Requirements

- A card must relate to a learning objective within a unit.
- Card requires cannot form a cycle.
- All cards must have a name (title) field.

### Card Guidelines

- Cards can require other cards.
- Cards can vary in length, but generally should be shorter than 10 minutes.
- Cards can vary greatly in the fields they contain, on basis of kind.

Units
-----

A unit is the medium size in the Sagefy data structure system. A unit represents a unit of learning activity.

A unit is defined by a single goal (objective). See [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom's_taxonomy). A unit should represent a goal that is as small as possible without becoming systemically redundant.

An example of a unit is a small learning lesson, which may contain about five to eight minutes of information and 30-60 minutes of practice to gain proficiency.

### Unit Requirements

- Units are language specific.
- Units must be the same language as the set.
- A unit must have a name.
- Must describe a specific learning objective that can't be easily subdivided.
- Unit requires cannot form a cycle.

### Unit Guidelines

- The unit goal should be described to the learner at the beginning.
- The current goal must be available to the learner at all times.
- Can establish required (prerequisite) units. (Keep it very specific.)
- A unit may also represent an **integration** of other units. In this case, a  tree would automatically form.
- A unit can be associated with a large number of cards.
- Some unit tags may include Bloom's Taxonomy

Sets
----

A set is a collection of units and other sets.

Sets can vary greatly in scale. For example, a small statistics set may cover central tendency, while a larger statistics set may cover descriptive statistics, while a very large set may cover a full statistics course series.

A graph is automatically formed based on the units and sets specified. Any chaining units or sets or necessary learner requirements would be automatically included.

### Set Requirements

- A set must contain at least one unit or set.
- A set must have a name and a body (description).

### Set Guidelines

- Most sets should be described as either a collection of "base" units or a collection of sets.
- Sets, unlike cards and units, cannot have requires. Those are automated computed.
