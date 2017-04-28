const {div, h1} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')

module.exports = function createUnitList() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add Units to Set'),
        unitWizard('list')

        // List of units with remove buttons
        // :: confirm to remove

        // Add an existing unit to set button
        // Create a new unit for set button

        // Back to choose a set
        // Create units button
    )
}
