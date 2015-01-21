View = require('../../framework/view')

###

Options

- name           required
- options        either options or url are required
- url            (default: null)
- showClear      (default: false for 0 or 1, true for 2+)
- chooseMultiple (default: false)
- showInline     (default: false)
- showOverlay    (default: false 0-6, true 7+)
- showSearch     (default: false 0-20 and not url, true 21+ or url)

###

class SelectView extends View
    className: 'select'
    template: ''
    domEvents: {

    }

    constructor: ->
        super

    render: ->
        super
        return this

module.exports = SelectView
