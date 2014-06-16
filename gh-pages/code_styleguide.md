---
title: Code Styleguide
layout: default
---

This document covers basic code styling and notes for Sagefy.

Global Code Styling
-------------------

- Four spaces per tab, unless its a generated file where that is the norm.
- No extra whitespace at the ends of lines.
- A single line break at the end of the file.
- A maximum of 79 characters per line.

Naming Conventions
------------------

- **Underscores**: Filenames, URLs, Database names, Python other than class names
- **Camelcase**: CoffeeScript, Python class names
- **Dashes**: Stylus, HTML attributes

Python
------

- In general, we use [Flake8](https://flake8.readthedocs.org/en/2.0/) for Python formatting.
    - Flake8 is the merger of [pep8](https://github.com/jcrocholl/pep8) and [PyFlakes](https://launchpad.net/pyflakes).
- Methods should be no longer than 12 statements.
- See [RESTish](/restish).
- DocStrings should follow [PEP-0257](http://legacy.python.org/dev/peps/pep-0257/) and when relevant the [NumPy convention](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt).
- _TODO_: URL formatting.
- _TODO_: Query parameter formatting.
- _TODO_: JSON response formatting.
    - Try to match the [Google JSON Styleguide](http://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml)
    - Put verbs in params: `_method`
    - See [ember.js](http://emberjs.com/guides/models/the-rest-adapter/) models too
- Database naming and conventions.
    - IDs are always randomly generated strings, String(64).
    - Include `created` and `modified`, using those exact names, when sensible.
    - Use `name` for title, name, or subject, `body` for body, message, description... Use String(256) for `name` and Text for `body`.
    - `language` is String(2)
    - Use `kind` for kind or type.
    - Use foreign keys.
    - Table names use all plural, column names are singular. Model names are singular. Use underscores.
    - Don't use negative named booleans. Stay positive :)


Coffeescript
------------

- See [Coffeelint](http://www.coffeelint.org/) for basic Coffeescript formatting.
- See [Coffeescript Style Guide](https://github.com/polarmobile/coffeescript-style-guide).
- Docstrings formatted in [Codo](https://github.com/coffeedoc/codo).

Stylus
------

- Use the least amount of syntax possible.
- Add comments in [YM Styleguide](https://github.com/heiskr/ym-styleguide).
- Use the [BEM](http://bem.info/method/) naming convention.
- Borrow ideas from the [SMACSS](http://smacss.com/) organization scheme.
- General guidelines:
    - Lowercase selectors.
    - Use extend first.
    - No duplicate properties.
    - Empty line after blocks of properties.
    - No empty rules.
    - Use leading zeros.
    - Merge selectors.
    - Don't go more than 3 levels deep.
    - Hyphen for names.
    - Spell correctly.
    - Use shorthands.
    - Space after commas.
    - Zero is unitless.

HTML
----

- The least markup possible.
- Use `ui-` for classes that interact with JavaScript/Coffeescript; plain classes are styling only.

Writing Tests
-------------

Basic rules for automated tests:

**1) Tests what matters**

It's too easy to get to get caught up in isolating everything for unit testing, writing a sea of functional tests, arguing over what type of test a test is, and gaming the coverage tool. Instead, simply tests what matters, and don't test what doesn't. If you don't care that the test fails, then don't write it.

**2) Use the context**

If it needs to work under a variety of conditions, isolate it. If it has a hard dependency, include it. If it needs to happen in less than 200 ms, ensure that it does. Write the test using the writing styles and tools appropriate for what matters.

**3) If something becomes an issue, write a test for it**

We don't want issues to recur. That also means we can write fewer tests up-front if we know new tests will be created as needed later.

**4) Describe the tests, write the code, write the tests**

It's hard to know how we implement things ahead of time. Describe the tests that matter first, then write the code, then write the test. It sounds a little backwards, but it takes less time and produces the same result.

Ansible and Configuration
-------------------------

- _TODO_

Other Documentation
-------------------

- Use [Markdown](https://daringfireball.net/projects/markdown/) when possible as the default.

