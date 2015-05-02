describe('Listener', ->
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
