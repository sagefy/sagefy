const {div, h1} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')

module.exports = function createUnitAdd() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add an Existing Unit to Set'),
        unitWizard('list')

        // Search box and button
        // List of units with add buttons
        // Back to list view button
    )
}