const {div, h1} = require('../../modules/tags')
const {cardWizard} = require('./create_shared.fn')

module.exports = function createCardCreate() {
    return div(
        {id: 'create', className: 'page'},
        h1('Create a New Card for Unit'),
        cardWizard('list')
    )
}
