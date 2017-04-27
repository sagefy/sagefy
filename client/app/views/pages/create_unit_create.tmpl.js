const {div, h1} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')

module.exports = function createUnitCreate() {
    return div(
        {id: 'create', className: 'page'},
        h1('Create a New Unit for Set'),
        unitWizard('list')
    )
}
