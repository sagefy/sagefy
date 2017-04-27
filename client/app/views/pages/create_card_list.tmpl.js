const {div, h1} = require('../../modules/tags')
const {cardWizard} = require('./create_shared.fn')

module.exports = function createCardList() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add Cards to Unit'),
        cardWizard('list')
    )
}
