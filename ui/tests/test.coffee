window.$ = require('jquery')

window.sinon = require('sinon')
window.sinonChai = require('sinon-chai')
chai.use(sinonChai)

mocha.setup('bdd')
window.expect = chai.expect

# Include tests here
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

require('./models/menu')
require('./views/menu')

# End include tests

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
