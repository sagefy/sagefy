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

Infrastructure
--------------

- **Server**: [Ansible](http://www.ansible.com/) with [Vagrant](http://www.vagrantup.com/)
    - **CDN**: [CloudFlare](https://www.cloudflare.com/)
    - [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/) on [Nginx](http://wiki.nginx.org/Main)
- **Language**: [Python 2.7](http://docs.python.org/2.7/)
- **Web framework**: [Flask](http://flask.pocoo.org/)
    - See [RESTish](/docs/restish)
- **User & Content Database**: [PostgreSQL](http://www.postgresql.org/docs/9.1/interactive/index.html)
- **Memory, ORM caching**: [Redis](http://redis.io/documentation)
- **Search**: [ElasticSearch](https://github.com/elasticsearch/elasticsearch)
- **Primary ORM**: [SQLAlchemy](http://www.sqlalchemy.org/) with [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
- **Migrations**: [Alembic](http://alembic.readthedocs.org/en/latest/)
- **Documentation**: [Jekyll](http://jekyllrb.com/) on [Github Pages](https://pages.github.com/)
    - **API Doc**: [Sphinx](http://sphinx-doc.org/) from inline docstrings using the [NumPy](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt) convention
    - **Versioning**: [SemVer](http://semver.org/) with [Version Badge](http://badge.fury.io/)
- **Deployment**: [Fabric](http://docs.fabfile.org/en/1.8/)
- **Version control**: [GitHub](http://github.com/)
- **Machine learning**: [NumPy](http://www.numpy.org/) + [SciPy](http://www.scipy.org/) + [Scikit-Learn](http://scikit-learn.org/stable/)
- **Continuous integration**: [TravisCI](https://travis-ci.org/) or [Semaphore](https://semaphoreapp.com/) or [Scrutinizer](https://scrutinizer-ci.com/)  _TODO:_ Choose one
- **Dependency manager**: [DavidDM](https://david-dm.org/)
- **Blogging**: [Wordpress.com](http://wordpress.com)
- **Feedback**: Github Issues, [StackOverflow](http://stackoverflow.com), [UserVoice](http://uservoice.com)
- **Project Management**: Github Issues with [Waffle.io](https://waffle.io/heiskr/sagefy)
- **Media page**: [Totemapp](http://totemapp.com)
- **Social**: [Twitter](http://twitter.com/sagefyorg), [Facebook](https://www.facebook.com/sagefy), [Google+](https://plus.google.com/102422704401628739470/posts), Github, [Wordpress](http://sagefy.wordpress.com/)
- **Analytics**: [Google Analytics](http://google.com/analytics) & in-house
- **Email accounts**: [Google Apps](http://apps.google.com)
- **Cloud storage**: [Google Drive](http://drive.google.com), [Dropbox](http://dropbox.com)
- **Authentication & Authorization**: Traditional Login + [OAuth2.0](http://oauth.net/2/)
- **Events, messaging, queues**: [Celery](http://www.celeryproject.org/), [RabbitMQ](http://www.rabbitmq.com/), Redis
- **Database admin** - [Flask admin](https://github.com/mrjoes/flask-admin/)
- **Package management** - [pip](https://pypi.python.org/pypi/pip), [npm](https://npmjs.org/), [bower](http://bower.io/)
- **Interface Formatting**
    - Try to match the [Google JSON Styleguide](http://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml)
    - Put verbs in params: `_method`
    - See [ember.js](http://emberjs.com/guides/models/the-rest-adapter/) models too
- **Test suites**
    - -
    - Python:
        - Unit, BDD: [py.test](http://pytest.org/latest/)
        - Lint: [Flake8](https://pypi.python.org/pypi/flake8)
        - Coverage: [Coverage.py](http://nedbatchelder.com/code/coverage/)
        - Mock: [Faker](https://github.com/joke2k/faker)
        - Performance: _TODO_
        - Security: _TODO_
        - i18n: _TODO_
    - Script:
        - Unit, BDD: [Mocha](http://visionmedia.github.io/mocha/)
        - Lint: [CoffeeLint](http://www.coffeelint.org/); also see [JSHint](http://www.jshint.com/)
        - Styleguide: Inhouse, based on [Coffeescript Style Guide](https://github.com/polarmobile/coffeescript-style-guide)
        - Coverage: [Blanket](http://blanketjs.org/)
        - Mock: [Chance.js](http://chancejs.com/)
        - Performance: _TODO_
        - i18n: _TODO_
        - Error reporting: _TODO_
    - Style:
        - Visual: [PhantomCSS](https://github.com/Huddle/PhantomCSS)
- **Transactional email** - [Mandrill](http://mandrill.com/), then [Postfix](http://www.postfix.org/)
- **UIs**
    - Style compiler - [Stylus](http://learnboost.github.io/stylus/)
    - Style framework, boilerplate - Custom, based on [TWBootstrap](http://getbootstrap.com/), [HTML5 B](http://html5boilerplate.com/), and [Foundation](http://foundation.zurb.com/)
    - Script MVC -[Backbone.js](http://backbonejs.org/) with (Marionette)[http://marionettejs.com/]
    - Script frameworks - [Coffeescript](http://coffeescript.org/), [jQuery](http://jquery.com/),  , [Modernizr](http://modernizr.com/)
    - Script utilities - _TODO_ [Select2](http://ivaynberg.github.io/select2/), [Moment](http://momentjs.com/), [Uglify](https://github.com/mishoo/UglifyJS), [Intro.js](http://usablica.github.io/intro.js/), [Selectize](http://brianreavis.github.io/selectize.js/), [Backgrid](http://backgridjs.com/), [Listjs](http://listjs.com/), [Dynatable.js](http://www.dynatable.com/)
    - Script data visualization - [D3.js](http://d3js.org/)
    - Form validation plugin - [jQuery Validation](http://jqueryvalidation.org/) or [backbone forms](https://github.com/powmedia/backbone-forms) or custom
    - Script documentation - [Codo](https://github.com/coffeedoc/codo)
    - Style documentation - [YM Styleguide](https://github.com/heiskr/ym-styleguide)
    - Style architecture - [BEM](http://bem.info/method/) and [SMACSS](http://smacss.com/)
    - Script templates - [Handlebars](http://handlebarsjs.com/); _TODO_ also test out [Jade](http://jade-lang.com/)
    - User content template system - [Markdown](http://daringfireball.net/projects/markdown/)
        - Add extensions for [Math](http://www.mathjax.org/), Footnotes, [Tables](https://github.com/chjj/marked#tables), Code, [Graphviz Dot](https://github.com/mdaines/viz.js), [Media Embeds](http://sloblog.io/+sloblog/qhdsk2SMoAU/sloblog-dot-io-easy-oembed-powered-media-embeds), and Definition Lists
        - [EpicEditor](https://github.com/OscarGodson/EpicEditor) with [Marked](https://github.com/chjj/marked) and [MathJax](http://www.mathjax.org/) or [Ace](http://ace.c9.io/) also see [LaTeX2HTML5](http://latex2html5.com/)
    - Compilation - [Gulp](http://gulpjs.com/) & [Bower](http://sindresorhus.com/bower-components/), [Require.js](http://requirejs.org/) (AMD)
    - Search engine access - [Node SEO Server](https://npmjs.org/package/seoserver)
- **Monitoring** - [Pingdom](https://www.pingdom.com/), [New Relic](http://newrelic.com/) (Free)
- _hold_ User research tools
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
- _TODO_ Analytics Databases (Mongo? PostgreSQL? Hadoop? Neo4J? Riak? http://influxdb.org/?)

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
