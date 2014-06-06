MenuView = require('../../scripts/views/menu')
MenuModel = require('../../scripts/models/menu')
$ = require('jquery')

describe('Menu View', ->
    before(->
        @model = new MenuModel()
        @view = new MenuView({model: @model})
        @$test = $('#test')
        @$test.append(@view.$el)
    )

    after(->
        @view.remove()
        delete @model
        delete @view
    )

    it('should open when the icon is clicked', ->
        @$test.find('.menu__trigger').click()
        expect(@view.$el).to.have.class('selected')
    )

    it('should close when the overlay is clicked', ->
        @$test.find('.menu__overlay').click()
        expect(@view.$el).to.not.have.class('selected')
    )

    it('should close when the icon is clicked again', ->
        @$test.find('.menu__trigger').click().click()
        expect(@view.$el).to.not.have.class('selected')
    )

    it('should render a list of menu items, given a model', ->
        expect(@view.$el.find('.menu__item')).to.exist
    )

    it('should show a title and icon for each menu item', ->
        $menuItem0 = @view.$el.find('.menu__item').first()
        expect($menuItem0).to.have('i.fa')
        expect($menuItem0).to.have('.menu__item__title')
    )

    it('should go to the related page when clicking a menu item', ->
        $menuItem0 = @view.$el.find('.menu__item').first()
        expect($menuItem0.find('a')).to.have.attr('href')
    )
)

