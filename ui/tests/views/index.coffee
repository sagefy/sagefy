IndexView = require('../../scripts/views/index')
$ = require('jquery')
require('jquery.cookie')

describe('Index View', ->
    before(->
        @$test = $('#test')
        @view = new IndexView({$region: @$test})
    )

    after(->
        @view.remove()
        $.removeCookie('logged_in', { path: '/' })
    )

    it('should show login or signup on logged out', ->
        $.cookie('logged_in', '0', {expires: 7, path: '/'})
        @view.render()
        expect(@$test.find('a[href*="/login"]')).to.exist
    )

    it('should show links to sections on logged in', ->
        $.cookie('logged_in', '1', {expires: 7, path: '/'})
        @view.render()
        expect(@$test.find('a[href*="/learn"]')).to.exist
    )
)
