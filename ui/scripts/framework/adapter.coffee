Events = require('./events')

###
The adapter is responsible for
- handling a route,
- creating instances of models and views,
- handling model and view events, and
- cleaning up after the route is finished.
###

###
TODO:
- Write tests
###

class Adapter extends Events
    # The app fetches the URLs from the adapters and registers them
    # with the router
    url: ''

    # **constructor**
    # When a route is hit, the constructor will be called.
    # Here, models and views should be defined, and listeners to the
    # views and models should bind here.
    # Additional methods can be defined to handle model and view events.

    # **remove**
    # When a different route is hit, the current adapter is removed.
    # Here, clean up the models, views, and event bindings.

module.exports = Adapter
