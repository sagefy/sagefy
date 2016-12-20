
Requirements
------------

- All entities must have a name.
- All entities are language specific.

### Card

- A card must belong to a single unit.
- A card must belong to a single unit of the same language.
- A card can have requires (prerequisites). Requires cannot form a cycle.
- Each card kind has its own set of requirements.
- For more card kinds, see [[Data Structure: Card Kinds]]. 

### Unit

- A unit must have a written goal.
- A unit must be a single learning objective than cannot be easily divided.
- A unit must have at least 2 cards to be active.
- A unit can have requires (prerequisites). Requires cannot form a cycle.

### Set

- A set must have a written goal.
- A set's goal can be anywhere from narrow to broad.
- A set must contain at least one unit or set.
- Sets may only contain units and sets of the same language.
- Sets, unlike cards and units, cannot have requires. Instead, sets have members. Membership cannot form a cycle.

Guidelines
----------

### Card

- Cards should be shorter than 3 minutes, but may vary in length.
- Based on kind, cards can vary greatly in the fields they contain.

### Unit

- A unit may also represent an **integration** of other units.
- Some unit tags may include [Bloom's Taxonomy](https://en.wikipedia.org/wiki/Bloom's_taxonomy).

### Set

- Most sets should be described as either a collection of units or a collection of sets.