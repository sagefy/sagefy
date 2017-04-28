const {div, h1} = require('../../modules/tags')
const {cardWizard} = require('./create_shared.fn')

module.exports = function createCardList() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add Cards to Unit'),
        cardWizard('list')

        // List of cards with remove buttons
        // :: confirm to remove

        // Create a new card for unit button

        // Back to choose a unit
        // Create cards button
    )
}
