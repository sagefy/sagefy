---
layout: docs
title: Data Structure> Requirements and Guidelines
---

## Requirements

- All entities must have a name.
- All entities are language specific.

### Card

- A card must belong to a single unit.
- A card must belong to a single unit of the same language.
- A card can have requires (prerequisites). Requires cannot form a cycle.
- Each card kind has its own requirements.
- For more card kinds, see [Data Structure: Card Kinds](Data-Structure-Card-Kinds).

### Unit

- A unit must have a written goal.
- A unit must be a single learning objective than cannot be easily divided.
- A unit must have at least 2 cards to be active.
- A unit can have requires (prerequisites). Requires cannot form a cycle.

### Subject

- A subject must have a written goal.
- A subject's goal can be anywhere from narrow to broad.
- A subject must contain at least one unit or subject.
- Subjects may only contain units and subjects of the same language.
- Subjects, unlike cards and units, cannot have requires. Instead, subjects have members. Membership cannot form a cycle.

## Guidelines

### Card

- Cards should be shorter than 3 minutes, but may vary in length.
- Based on kind, cards can vary greatly in the fields they contain.

### Unit

- A unit may also represent an **integration** of other units.
- Some unit tags may include [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom's_taxonomy).

### Subject

- Most subjects should be described as either a collection of units or a collection of subjects.
