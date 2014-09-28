View = require('../../framework/view')
template = require('../../templates/layouts/form')

class FormLayoutView extends View
    template: template
    elements: {
        'form': '.form'
    }

module.exports = FormLayoutView
