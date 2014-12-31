Contributing
------------

Thank you for contributing to Sagefy! This document covers basic guidelines for contributing to Sagefy.

Issues
------

- Please search the existing issues before submitting. This helps us reduce effort and prioritize.
- For bug reports, to make the process as smooth as possible, please provide:
    - Step-by-step how to reproduce.
    - Screenshots.
    - Logs, as available.
- For feature requests, consider adding it to [UserVoice](http://sagefy.uservoice.com/) instead. On UserVoice, the feature can be discussed and prioritized more easily.

Pull Request Checklist
----------------------

For each pull request, ensure:

- ...the code passes linters as documented below.
- ...the code passes existing automated tests.
- ...each method is documented according to the given domain.
- ...the code follows the code styleguide below.
- ...the code has some basic test coverage, where appropriate.
- ...another person has reviewed the code.

Global Code Styling
-------------------

- Four spaces per tab, unless its a generated file where two is the norm.
- No extra whitespace at the ends of lines.
- A single line break at the end of the file.
- A maximum of 80 characters per line.

Naming Conventions
------------------

- **Underscores**: Filenames, URLs, Database names, Python other than class names
- **Camelcase**: CoffeeScript, Python class names
- **Dashes**: Stylus, HTML attributes

Python
------

- Use [Flake8](https://flake8.readthedocs.org/en/2.0/) for Python formatting.
    - Flake8 is the merger of [pep8](https://github.com/jcrocholl/pep8) and [PyFlakes](https://launchpad.net/pyflakes).
- Methods should be no longer than 12 statements.
- Request and response formatting: see [RESTish](https://docs.sagefy.org/f_technology/restish).
- DocStrings should follow [PEP-0257](http://legacy.python.org/dev/peps/pep-0257/) and when relevant the [NumPy convention](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt).

Database
--------

- Database naming and conventions.
- IDs are always randomly generated strings.
- Include `created` and `modified`, using those exact names, when sensible.
- Use `name` for title, name, or subject.
- Use `body` for body, message, description..
- Use `kind` for kind or type.
- When the number of kinds is unknown, use `tags` instead.
- Use `_tablename` to refer to the name of another table.
- Table names use all plural, field names are singular. Model names are singular. Use underscores.
- Multiple join tables should use both names, and both in plural form.
- When the relationship is...
- 1 to 1: Should probably use embedding. Otherwise, use the same ID for both.
- 1 to many: Put the "1" ID into the "many" rows.
- Many to many: Embed IDs, otherwise use a join table.
- Don't use negative named booleans. Stay positive.

Coffeescript
------------

- See [Coffeelint](http://www.coffeelint.org/) for basic Coffeescript formatting.
- See [Coffeescript Style Guide](https://github.com/polarmobile/coffeescript-style-guide).
- Write concise comments before classes, methods, blocks.

Stylus
------

- Use the least amount of syntax possible.
- Add comments in [YM Styleguide](https://github.com/heiskr/ym-styleguide).
- Use the [BEM](http://bem.info/method/) naming convention where appropriate.
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
- TODO: Use `ui-` for classes that interact with JavaScript/Coffeescript; plain classes are styling only.

Writing Tests
-------------

Basic guidelines for automated tests:

**1) Tests what matters**

It's too easy to get to get caught up in isolating everything for unit testing, writing a sea of esoteric tests, arguing over what type of test a test is, and gaming the coverage tool. Instead, simply tests what matters, and don't test what doesn't. If you don't care that the test fails, then don't write it.

**2) Use the context**

If it needs to work under a variety of conditions, isolate it. If it has a hard dependency, include it. If it needs to happen in less than 200 ms, ensure that it does. Write the test using the writing styles and tools appropriate for what matters.

**3) If something becomes an issue, write a test for it**

We don't want issues to recur. That also means we can write fewer tests up-front if we know new tests will be created as needed later.

**4) Describe the tests, write the code, write the tests**

It's hard to know how we implement things ahead of time. Describe the tests that matter first, then write the code, then write the test. It sounds a little backwards, but it takes less time and produces the same result.

Ansible and Configuration
-------------------------

- Use the `setup` directory.
- More guidelines TBD.

Other Documentation
-------------------

- Use [Markdown](https://daringfireball.net/projects/markdown/) when possible as the default.
