window.$ = window.jQuery = require('jquery')

window.chai = require('chai')

window.sinon = require('sinon')
require('sinon/lib/sinon/util/event')
require('sinon/lib/sinon/util/fake_xml_http_request')
window.sinonChai = require('sinon-chai')
chai.use(sinonChai)

window.chaiJQuery = require('chai-jquery')
chai.use(chaiJQuery)

mocha.setup('bdd')
window.expect = chai.expect

# Include tests here
require('./basic')

require('./framework/events')
require('./framework/utilities')
require('./framework/adapter')
require('./framework/validations')
require('./framework/model')
require('./framework/collection')
require('./framework/view')
require('./framework/list_view')
require('./framework/layout_view')
require('./framework/application')

require('./routers/base')
require('./routers/index')

require('./controllers/base')

###
require('./modules/hbs_helpers')
require('./modules/mixins')

require('./models/menu')
require('./models/user')

require('./views/password')
require('./views/error')
require('./views/form')
require('./views/index')
require('./views/login')
require('./views/logout')
require('./views/menu')
require('./views/settings')
require('./views/signup')
require('./views/styleguide')
###

# End include tests

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
