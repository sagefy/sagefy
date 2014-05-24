---
title: Technology
layout: default
---

This document lists technology that Sagefy uses and intends to use.

Development Checklist
---------------------

For each pull request, ensure the following:

- General follows [code styleguide](/docs/code_styleguide).
- Each method is documented according to the system for the given domain
- Code passes used linters
- Passes existing automated tests (run CI automatically on pull requests)
- Reviewed by a person
- Provides some basic unit test coverage, where appropriate
- Provides some basic functional test coverage, where appropriate

We Use
------

- Building and Serving
    - [Vagrant](http://www.vagrantup.com/)
    - [CloudFlare](https://www.cloudflare.com/)
    - [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/)
    - [Nginx](http://wiki.nginx.org/Main)
- Databases
    - [PostgreSQL](http://www.postgresql.org/docs/9.1/interactive/index.html)
    - [Redis](http://redis.io/documentation)
- API
    - [pip](https://pypi.python.org/pypi/pip)
    - [Python 2.7](http://docs.python.org/2.7/)
    - [Flask](http://flask.pocoo.org/)
    - [SQLAlchemy](http://www.sqlalchemy.org/)
        - [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
        - [Alembic](http://alembic.readthedocs.org/en/latest/)
    - Testing
        - [py.test](http://pytest.org/latest/)
        - [Flake8](https://pypi.python.org/pypi/flake8)
- UI
    - [npm](https://npmjs.org/)
    - [Gulp](http://gulpjs.com/)
        - [CoffeeLint](http://www.coffeelint.org/)
        - [Browserify](http://browserify.org/)
    - [Stylus](http://learnboost.github.io/stylus/)
    - [Backbone.js](http://backbonejs.org/)
    - [Coffeescript](http://coffeescript.org/)
    - [Handlebars](http://handlebarsjs.com/)
    - [BEM](http://bem.info/method/)
    - [YM Styleguide](https://github.com/heiskr/ym-styleguide)
    - Testing
        - [Mocha](http://visionmedia.github.io/mocha/)
        - [Chai](http://chaijs.com/)
        - [Sinon](http://sinonjs.org/)
- Project Management, Documentation
    - [GitHub](http://github.com/)
        - Github Issues with [Waffle.io](https://waffle.io/heiskr/sagefy)
    - [Jekyll](http://jekyllrb.com/) on [Github Pages](https://pages.github.com/)
    - [Markdown](http://daringfireball.net/projects/markdown/)

We Intend to Use
----------------

- Building and Serving
    - [Ansible](http://www.ansible.com/)
    - [Fabric](http://docs.fabfile.org/en/1.8/)
    - [TravisCI](https://travis-ci.org/) or [Semaphore](https://semaphoreapp.com/) or [Scrutinizer](https://scrutinizer-ci.com/)  _TODO:_ Choose one
    - [DavidDM](https://david-dm.org/)
    - [Pingdom](https://www.pingdom.com/)
    - [New Relic](http://newrelic.com/) (Free)
- Databases
    - [ElasticSearch](https://github.com/elasticsearch/elasticsearch)
- API
    - [NumPy](http://www.numpy.org/) + [SciPy](http://www.scipy.org/) + [Scikit-Learn](http://scikit-learn.org/stable/)
    - [Sphinx](http://sphinx-doc.org/) from inline docstrings using the [NumPy](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt) convention
    - Testing
        - [Coverage.py](http://nedbatchelder.com/code/coverage/)
        - [Faker](https://github.com/joke2k/faker)
    - Traditional Login + [OAuth2.0](http://oauth.net/2/)
    - [Celery](http://www.celeryproject.org/), [RabbitMQ](http://www.rabbitmq.com/), Redis
    - [Flask admin](https://github.com/mrjoes/flask-admin/)
    - [Mandrill](http://mandrill.com/), then [Postfix](http://www.postfix.org/)
- UI
    - JS error reporting _TODO_
    - [Codo](https://github.com/coffeedoc/codo)
    - [D3.js](http://d3js.org/)
    - Script utilities - _TODO_ [Select2](http://ivaynberg.github.io/select2/), [Moment](http://momentjs.com/), [Uglify](https://github.com/mishoo/UglifyJS), [Intro.js](http://usablica.github.io/intro.js/), [Selectize](http://brianreavis.github.io/selectize.js/), [Backgrid](http://backgridjs.com/), [Listjs](http://listjs.com/), [Dynatable.js](http://www.dynatable.com/)
    - Markdown; Add extensions for [Math](http://www.mathjax.org/), Footnotes, [Tables](https://github.com/chjj/marked#tables), Code, [Graphviz Dot](https://github.com/mdaines/viz.js), [Media Embeds](http://sloblog.io/+sloblog/qhdsk2SMoAU/sloblog-dot-io-easy-oembed-powered-media-embeds), and Definition Lists
    - [EpicEditor](https://github.com/OscarGodson/EpicEditor) with [Marked](https://github.com/chjj/marked) and [MathJax](http://www.mathjax.org/) or [Ace](http://ace.c9.io/) also see [LaTeX2HTML5](http://latex2html5.com/)
    - Testing
        - [Blanket](http://blanketjs.org/)
        - [Chance.js](http://chancejs.com/)
        - [PhantomCSS](https://github.com/Huddle/PhantomCSS)
    - User Research
        - Split test _TODO_
        - Accessibility _TODO_
        - [Card sort](http://conceptcodify.com)
        - Prototype testing _TODO_
        - [Heatmap](http://www.crazyegg.com/)
        - Mobile testing _TODO_
        - Remote usability _TODO_
        - [Surveying](http://surveymonkey.com)
        - Web Analytics - Google Analytics
        - Wireframes & diagrams _TODO_
- Project Management, Documentation
    - [SemVer](http://semver.org/) with [Version Badge](http://badge.fury.io/)
    - [Google Analytics](http://google.com/analytics) & in-house
    - [Google Apps](http://apps.google.com)
    - [Google Drive](http://drive.google.com), [Dropbox](http://dropbox.com)
- Outreach
    - [Wordpress.com](http://wordpress.com)
    - Github Issues, [StackOverflow](http://stackoverflow.com), [UserVoice](http://uservoice.com)
    - [Totemapp](http://totemapp.com)
    - [Twitter](http://twitter.com/sagefyorg), [Facebook](https://www.facebook.com/sagefy), [Google+](https://plus.google.com/102422704401628739470/posts), Github, [Wordpress](http://sagefy.wordpress.com/)

## Sections

- Core (API)
    - API core build first, separate from UIs
    - Database, Analysis
- Contribute UI
    - Interface for uploading content, practice, and designing application
    - Developing content relationships
    - Content feedback and peer review
- Learn UI
    - Primary learner interface
    - Learner data and progress
    - Most adaptive UI, language, technology, location...
- Analyze UI
    - Open anonymous statistics
    - Large-to-small picture
    - Useful for data scientists and educational scientists
    - Allows some querying
- Moderate UI
    - Additional interface for moderating discussion, content, conflicts
    - Promote conflict resolution strategies
    - Use democracy
- Mentor UI
    - Interface for learning by teaching
    - Answer learner questions on given topic
    - Suggest content changes by learner issues

Routing
-------

### ui/index.html

- `/`, `/login`, `/settings`, `/logout`, `/terms`, `/contact`
- `/learn`, `/learn/*`
- `/contribute`, `/contribute/*`
- `/analyze`, `/analyze/*`
- `/moderate`, `/moderate/*`
- `/mentor`, `/mentor/*`

### api/index.py

- `/api/*`

### External applications

- `/blog`, `/support`, `/questions`, `/feedback`, `/docs`, `/api/docs`
