const {div, h1} = require('../../modules/tags')

module.exports = function createSetCreate() {
    return div(
        {id: 'create', className: 'page'},
        h1('Create a New Set')
    )
}
