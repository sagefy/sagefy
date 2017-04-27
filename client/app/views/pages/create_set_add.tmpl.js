const {div, h1} = require('../../modules/tags')

module.exports = function createSetAdd() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add an Existing Unit or Set to New Set')
    )
}
