$ = require('jquery')

# Include tests here
describe('module', ->
    it('to run a test', ->
        expect(true).to.be.true
    )

    it('to have jquery expect', ->
        expect($('#mocha')).to.have.id('mocha')
    )
)
