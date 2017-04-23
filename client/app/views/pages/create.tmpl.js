const {div} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')


module.exports = (/* data */) => {
    return div(
        {id: 'create', className: 'page'},
        icon('create')
    )
}
