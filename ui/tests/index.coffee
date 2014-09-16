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
require('./basic')

require('./framework/events')

require('./modules/hbs_helpers')
require('./modules/mixins')

require('./routers/base')
require('./routers/index')

require('./controllers/base')

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
# End include tests

if window.mochaPhantomJS
    mochaPhantomJS.run()
else
    mocha.run()
