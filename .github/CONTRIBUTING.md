# Contributing

Thank you for contributing to Sagefy! This document covers basic guidelines for contributing to Sagefy.

## Content

Create and edit content through the discussion section within the Sagefy interface. You will want to get familiar with the [Data Structure](https://github.com/heiskr/sagefy/wiki/Data-Structure).

## Pull Request Checklist

For each pull request:

* Review and agree to release the code under the terms in the [Apache 2.0 license](http://www.apache.org/licenses/LICENSE-2.0).
* Pass the linters and existing automated tests.
* Document each function.
* Follow the code styleguide, as documented below.
* Write at least one test per function.
* Let another person review the code.

## Global Code Styling

* Two spaces per tab.
* No extra whitespace at the ends of lines.
* A single line break at the end of the file.
* A maximum of 80 characters per line.

## Naming Conventions

* **Underscores**: Filenames, URLs, Database names, Python other than class names
* **Camelcase**: JavaScript, Python class names
* **Dashes**: Stylus, HTML attributes

## Python

* Use [Pylint](https://www.pylint.org/) for Python formatting.
* Methods are no longer than 12 statements.
* Request and response formatting: see [RESTish](https://github.com/heiskr/sagefy/wiki/RESTish).
* DocStrings follow [PEP-0257](http://legacy.python.org/dev/peps/pep-0257/) and when relevant the [NumPy convention](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt).

## Database

* Table names are plural.
* Field names are singular, unless an array.
* Join tables use both names, and both in plural form.
* Don't use negative named booleans. Stay positive.
* IDs are always randomly generated strings.
* Include `created` and `modified`, using those exact names, when sensible.
* Use `name` for title, name, or subject.
* Use `body` for body, message, description.
* Use `kind` for kind or type.
* When the number of kinds is unknown, use `tags` instead.
* When the relationship is...
  * 1 to 1: Probably use embedding. Otherwise, use the same ID for both.
  * 1 to many: Put the "1" ID into the "many" rows.
  * Many to many: Embed IDs, otherwise use a join table.

## JavaScript

* See [Eslint](http://www.eslint.org/) for basic JavaScript formatting.
* Write concise comments before classes, methods, blocks.

## Stylus

* Use the least amount of syntax possible.
* Add comments in [YM Styleguide](https://github.com/heiskr/ym-styleguide).
* Use the [BEM](http://bem.info/method/) naming convention where appropriate.
* Mobile is the first and default styling. Use `@media (min-width...)` and never use `@media (max-width...)`.
* General guidelines:
  * Lowercase selectors.
  * Use extend first.
  * No duplicate properties.
  * Empty line after blocks of properties.
  * No empty rules.
  * Use leading zeros.
  * Merge selectors.
  * Don't go more than 3 levels deep.
  * Hyphen for names.
  * Spell correctly.
  * Use shorthands.
  * Space after commas.
  * Zero is unitless.

## HTML

* The least markup possible.

## Writing Tests

Basic guidelines for automated tests:

**1) Tests what matters**

It's too easy to get to get caught up in isolating everything for unit testing, writing a sea of esoteric tests, arguing over what type of test a test is, and gaming the coverage tool. Instead, simply tests what matters, and don't test what doesn't. If you don't care that the test fails, then don't write it.

**2) Use the context**

If it needs to work under a variety of conditions, isolate it. If it has a hard dependency, include it. If it needs to happen in less than 200 ms, ensure that it does. Write the test using the writing styles and tools appropriate for what matters.

**3) If something becomes an issue, write a test for it**

We don't want issues to recur. That also means we can write fewer tests up-front if we know new tests will be created as needed later.

## Other Documentation

* Use [Markdown](https://daringfireball.net/projects/markdown/) when possible as the default.
