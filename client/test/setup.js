global.document = require('jsdom').jsdom()
global.window = document.defaultView
global.Element = window.Element
global.XMLHttpRequest = window.XMLHttpRequest

const chai = require('chai')
global.expect = chai.expect
global.sinon = require('sinon')
chai.use(require('sinon-chai'))
