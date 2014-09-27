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

require('./framework/events')
require('./framework/utilities')
require('./framework/adapter')
require('./framework/validations')
require('./framework/model')
require('./framework/collection')
require('./framework/view')
require('./framework/application')

require('./modules/mixins')

require('./models/user')
require('./models/menu')

### End include tests ###

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
