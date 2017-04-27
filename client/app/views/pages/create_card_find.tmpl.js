const {div, h1} = require('../../modules/tags')
const {cardWizard} = require('./create_shared.fn')

module.exports = function createCardFind() {
    return div(
        {id: 'create', className: 'page'},
        h1('Find a Unit to Add Cards'),
        cardWizard('find')
    )
}
