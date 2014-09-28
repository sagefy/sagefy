MenuModel = require('../../scripts/models/menu')

describe('Menu Model', ->
    beforeEach(->
        @model = new MenuModel()
        @model.state = 'loggedOut'
    )

    afterEach(->
        delete @model
    )

    it('should generate a list of menu items', ->
        expect(@model.items()).to.be.an('array')
        expect(@model.items()[0]).to.be.an('object')
        expect(@model.items()[0].name).to.be.a('string')
    )

    it('should have the right menu items on logged out', ->
        menuNames = @model.menus.loggedOut
        for i, menuName of menuNames
            expect(@model.items()[i].name)
                .to.equal(menuName)
    )

    it('should have the right menu items when logged in', ->
        @model.state = 'loggedIn'
        menuNames = @model.menus.loggedIn
        for i, menuName of menuNames
            expect(@model.items()[i].name)
                .to.equal(menuName)
    )

    it('should update the menu items when the state changes', ->
        @model.state = 'loggedOut'
        namesA = @model.items().map((o) -> return o.name)
        @model.state = 'loggedIn'
        namesB = @model.items().map((o) -> return o.name)
        expect(namesA).to.not.equal(namesB)
    )

    it('should allow setting a custom icon', ->
        @model._items.login.icon = 'taxi'
        expect(@model.items()[0].icon).to.equal('taxi')
    )

    it('should capitalize the page title', ->
        expect(@model.items()[0].title).to.equal('Log In')
    )

    it('should use underscores for URLs', ->
        @model._items['taxi-service'] = {}
        @model.menus.loggedOut.push('taxi-service')
        @model._items = @model._itemsBoilerplate(@_items)
        @model.updateState()
        expect(@model.items()[3].url).to.equal('/taxi_service')
    )
)
