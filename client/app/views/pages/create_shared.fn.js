const wizard = require('../components/wizard.tmpl')

module.exports = {
    unitWizard(state = 'find') {
        return wizard({
            options: [{
                label: 'Find Subject',
                name: 'find',
            }, {
                label: 'Add Units',
                name: 'list',
            }, {
                label: 'View',
                name: 'view',
            }],
            state,
        })
    },

    cardWizard(state = 'find') {
        return wizard({
            options: [{
                label: 'Find Unit',
                name: 'find',
            }, {
                label: 'Add Cards',
                name: 'list',
            }, {
                label: 'View',
                name: 'view',
            }],
            state,
        })
    },
}
