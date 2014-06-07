ErrorView = require('../../scripts/views/error')
$ = require('jquery')

describe('Error View', ->
    before(->
        @$test = $('#test')
        @view = new ErrorView({
            $region: @$test
            code: 404
            message: 'Not Found'
        })
    )

    after(->
        @view.remove()
    )

    it('should render an error matching a status code', ->
        expect(@$test.find('h1')).to.have.text('404')
    )
)
