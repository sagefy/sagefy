const {div, h1} = require('../../modules/tags')
const {cardWizard} = require('./create_shared.fn')

module.exports = function createCardFind() {
    return div(
        {id: 'create', className: 'page'},
        h1('Find a Unit to Add Cards'),
        cardWizard('find')

        // My Recent Units
        // List of units with √ buttons

        // - or -

        // Search box and buttons
        // List of units with √ buttons

        // Back to create page
    )
}
