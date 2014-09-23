hbs = require('handlebars')
require('../../scripts/modules/hbs_helpers')(hbs)

describe('Handlebars Helpers', ->
    ###
    N.B.: In this file we will tests specifically
    that Handlebars has these capabilities.
    We will not test if the functions run independently. See `mixins`.
    ###

    before(->
        @render = (template, values) ->
            return hbs.compile(template)(values)
    )

    after(->
        @render = null
    )

    it('should do something if an array contains a specified element', ->
        expect(
            @render('{{#contains arr 1}}true{{/contains}}', {arr: [1, 2, 3]})
        )
            .to.equal('true')
    )
)
