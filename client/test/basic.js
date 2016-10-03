describe('Basic test setup', () => {
    it('should run a test', () =>
        expect(true).to.be.true
    )

    it('should have sinon', () => {
        const spy = sinon.spy()
        spy('foo')
        expect(spy).to.have.been.calledWith('foo')
    })
})
