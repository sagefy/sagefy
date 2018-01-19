const jsdom = require('jsdom').jsdom()
const chai = require('chai')
const sinon = require('sinon')
const sinonChai = require('sinon-chai')

global.document = jsdom
global.window = document.defaultView
global.Element = window.Element
global.XMLHttpRequest = window.XMLHttpRequest

global.expect = chai.expect
global.sinon = sinon
chai.use(sinonChai)
