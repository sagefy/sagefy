StyleguideView = require('../../scripts/views/styleguide')
$ = require('jquery')

describe('Styleguide View', ->
    before(->
        @$test = $('#test')
        @view = new StyleguideView({$region: @$test})
    )

    after(->
        @$test.empty()
        @view.remove()
    )

    it('should add the compiled styleguide HTML to the page', ->
        expect(@$test.find('.sg-field')).to.exist
    )

    it('should open external links in a new window', ->
        $link = @$test.find('a[href*="//"]').first()
        $link.click()
        expect($link).to.have.attr('target')
    )
)
