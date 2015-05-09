View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class LogOutPageView extends View
    template: -> return '<div class="spinner"></div>'

    constructor: ->
        super
        aux.setTitle('Logging Out...')

        if aux.isLoggedIn()
            @on('logged out user', @toIndex)
            @emit('requested log out user')
        else
            @toIndex()

        @render()

    # Hard redirect to lose cookie
    toIndex: ->
        window.location = '/'

module.exports = LogOutPageView
