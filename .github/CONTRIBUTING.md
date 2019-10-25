# Contributing

Thank you for contributing to Sagefy! This document covers basic guidelines for contributing to Sagefy.

Not sure where to help out? We have some ideas in our [Want to Help](https://docs.sagefy.org/want-to-help) guide.

Reach out to support@sagefy.org for help!

## Content

Create and edit content through the discussion section within the Sagefy interface. You will want to get familiar with [Cards & Subjects](https://docs.sagefy.org/cards-subjects). More docs coming soon!

## Code

To start up your local development environment, please read our [Setup](https://docs.sagefy.org/setup) doc. You may also want to read [Cards & Subjects](https://docs.sagefy.org/cards-subjects), [User Stories](https://docs.sagefy.org/user-stories), [Technology Stack](https://docs.sagefy.org/technology-stack), and [Technical Architecture](https://docs.sagefy.org/technical-architecture).

### Pull Request Checklist

For each pull request:

- Review and agree to release the code under the terms in the [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0).
- Pass the linters and existing automated tests.
- Document each function.
- Follow the code styleguide, as documented below.
- Write at least one test per function.
- Let another person review the code.

### Global Code Styling

- Two spaces per tab.
- No extra whitespace at the ends of lines.
- A single line break at the end of the file.
- A maximum of 80 characters per line.

### Naming Conventions

- **Underscores**: Database names
- **Camelcase**: JavaScript
- **Dashes**: Filenames, URLs, CSS, HTML attributes
- _Create, Edit, Delete_: URLs, Page names, Attributes, User copy
- _Create, Update, Delete_: Postgres, GraphQL

### Database

- Table names are singular.
- Field names are singular, unless an array.
- Join tables use both names, and both in singular form.
- Don't use negative named booleans. Stay positive.
- IDs are always randomly generated strings.
- Include `created` and `modified`, using those exact names, when sensible.
- Use `name` for title, name, or subject.
- Use `body` for body, message, description.
- Use `kind` for kind or type.
- Use third normal form unless there's no query requirement.

### JavaScript

- See [Eslint](http://www.eslint.org/) for basic JavaScript formatting.

### Styles

- Mobile is the first and default styling. Use `@media (min-width...)` and never use `@media (max-width...)`.
- Explain the necessity of each additional styling.

### HTML

- The least markup possible.

### Other Documentation

- Use [Markdown](https://daringfireball.net/projects/markdown/) when possible as the default.
