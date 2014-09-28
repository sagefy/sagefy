window.chai = require('chai')

window.sinon = require('sinon')
require('sinon/lib/sinon/util/event')
require('sinon/lib/sinon/util/fake_xml_http_request')
window.sinonChai = require('sinon-chai')
chai.use(sinonChai)

mocha.setup('bdd')
window.expect = chai.expect

### Include tests here ###

require('./basic')
require('./framework')
require('./modules')
require('./models')
require('./templates')
require('./views')
require('./adapters')

### End include tests ###

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
