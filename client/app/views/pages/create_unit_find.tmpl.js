const {div, h1} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')

module.exports = function createUnitFind() {
    return div(
        {id: 'create', className: 'page'},
        h1('Find a Set to Add Units'),
        unitWizard('find')
    )
}
