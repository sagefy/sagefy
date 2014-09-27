View = require('../../framework/view')

class StyleguideView extends View
    events: {
        'click a[href="#"]': 'cancel'
        'click a[href*="//"]': 'openInNewWindow'
    }

    # Empty-ish links should go nowhere when clicked
    cancel: (e) ->
        e.preventDefault()

    # External links should automatically open in a new window
    openInNewWindow: (e) ->
        e.target.target = '_blank'

module.exports = StyleguideView
