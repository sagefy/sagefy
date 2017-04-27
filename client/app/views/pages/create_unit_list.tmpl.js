const {div, h1} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')

module.exports = function createUnitList() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add Units to Set'),
        unitWizard('list')
    )
}
