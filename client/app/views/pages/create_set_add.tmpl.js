const {div, h1} = require('../../modules/tags')

module.exports = function createSetAdd() {
    return div(
        {id: 'create', className: 'page'},
        h1('Add an Existing Unit or Set to New Set')
        // Search box and button
        // List of results with Add buttons
        // :: Add -> click to add then return to create view
        // Back to create set button
    )
}
