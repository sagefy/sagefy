describe('Basic test setup', ->
    it('should run a test', ->
        expect(true).to.be.true
    )

    it('should have chai jquery', ->
        expect($('#mocha')).to.have.id('mocha')
    )

    it('should have sinon', ->
        spy = sinon.spy()
        spy('foo')
        expect(spy).to.have.been.calledWith('foo')
    )
)
