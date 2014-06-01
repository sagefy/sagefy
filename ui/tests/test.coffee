window.sinon = require('sinon')
window.sinonChai = require('sinon-chai')
chai.use(sinonChai)

mocha.setup('bdd')
window.expect = chai.expect

# Include tests here
$ = require('jquery')
describe('module', ->
    it('to run a test', ->
        expect(true).to.be.true
    )

    it('to have jquery expect', ->
        expect($('#mocha')).to.have.id('mocha')
    )
)

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
