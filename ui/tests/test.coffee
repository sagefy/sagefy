window.$ = window.jQuery = require('jquery')

window.chai = require('chai')

window.sinon = require('sinon')
window.sinonChai = require('sinon-chai')
chai.use(sinonChai)

window.chaiJQuery = require('chai-jquery')
chai.use(chaiJQuery)

mocha.setup('bdd')
window.expect = chai.expect

# Include tests here
require('./test_basic')
require('./models/menu')
require('./views/menu')

# End include tests

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
