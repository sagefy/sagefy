Events = require('../../scripts/framework/events')

describe('Events', ->
    beforeEach(->
        @e = new Events()
        @ting = false
        @f = (a) =>
            @ting = a || true
        @z = new Events()
    )

    after(->
        delete @e
    )

    it('should register an event', ->
        @e.on('poke', @f)
        expect(@e.events.poke).to.be.an('array')
        expect(@e.events.poke[0]).to.be.a('function')
    )

    it('should register only one binding per event', ->
        @e.on('poke', @f)
        @e.on('poke', @f)
        expect(@e.events.poke).to.have.length(1)
    )

    it('should trigger an event', ->
        @e.on('poke', @f)
        expect(@ting).to.be.false
        @e.trigger('poke')
        expect(@ting).to.be.true
    )

    it('should ignore triggering an event with no handlers', ->
        @e.trigger('poke')
        expect(@ting).to.be.false
    )

    it('should provide arguments when triggering an event', ->
        @e.on('poke', @f)
        expect(@ting).to.be.false
        @e.trigger('poke', 'mushroom')
        expect(@ting).to.equal('mushroom')
    )

    it('should remove an event', ->
        @e.on('poke', @f)
        expect(@e.events.poke).to.have.length(1)
        @e.off('poke', @f)
        expect(@e.events.poke).to.be.empty
    )

    it('should remove all events', ->
        @e.on('poke', @f)
        expect(@e.events).to.not.be.empty
        @e.off()
        expect(@e.events).to.be.empty
    )

    it('should remove all events of a given type', ->
        @e.on('poke', @f)
        @e.on('sway', @f)
        @e.off('poke')
        expect(@e.events.poke).to.be.empty
        expect(@e.events.sway).to.have.length(1)
    )

    it('should listen to an event', ->
        @e.listenTo(@z, 'poke', @f)
        expect(@e.listeners).to.have.length(1)
        expect(@z.events.poke).to.have.length(1)
    )

    it('should stop listening to all event', ->
        @e.listenTo(@z, 'poke', @f)
        @e.stopListening()
        expect(@e.listeners).to.be.empty
        expect(@z.events.poke).to.be.empty
    )

    it('should stop listening to some events, based on name', ->
        @e.listenTo(@z, 'poke', @f)
        @e.stopListening({name: 'poke'})
        expect(@e.listeners).to.be.empty
        expect(@z.events.poke).to.be.empty
    )

    it('should stop listening to some events, based on object', ->
        @e.listenTo(@z, 'poke', @f)
        @e.stopListening({obj: @z})
        expect(@e.listeners).to.be.empty
        expect(@z.events.poke).to.be.empty
    )

    it('should stop listening to an event', ->
        @e.listenTo(@z, 'poke', @f)
        @e.stopListening({obj: @z, name: 'poke', fn: @f})
        expect(@e.listeners).to.be.empty
        expect(@z.events.poke).to.be.empty
    )

    it('should remove itself cleanly', ->
        @e.on('poke', @f)
        @e.listenTo(@z, 'poke', @f)
        @e.remove()
        expect(@e.events).to.be.empty
        expect(@e.listeners).to.be.empty
    )
)
