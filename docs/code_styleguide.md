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

Python
------

- In general, we use [Flake8](https://flake8.readthedocs.org/en/2.0/) for Python formatting.
    - Flake8 is the merger of [pep8](https://github.com/jcrocholl/pep8) and [PyFlakes](https://launchpad.net/pyflakes).
- Methods should be no longer than 12 statements.
- See [RESTish](/docs/restish).
- DocStrings should follow [NumPy convention]().
- _TODO_: URL formatting.
- _TODO_: Query parameter formatting.
- _TODO_: JSON response formatting.
    - Try to match the [Google JSON Styleguide](http://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml)
- _TODO_: Database naming and conventions.
- _TODO_: Writing tests.

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

HTML
----

- The least markup possible.
- Use `ui-` for classes that interact with JavaScript/Coffeescript; plain classes are styling only.

Ansible and Configuration
-------------------------

- _TODO_

Other Documentation
-------------------

- Use [Markdown](https://daringfireball.net/projects/markdown/) when possible as the default.

