$ = require('jquery')
FormView = require('./form')

class Settings extends FormView
    title: 'Settings'
    id: 'settings'
    className: 'max-width-6'
    fields: ['name', 'email']  # password, avatar, notifications
    description: 'All fields autosave.'
    edit: true

module.exports = Settings
