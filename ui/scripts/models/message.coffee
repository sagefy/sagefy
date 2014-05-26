Backbone = require('backbone')

class MessageModel extends Backbone.Model

    url: '/api/messages/'

    # [fields]
    # id
    # created
    # modified

    validate: (attrs, options) ->

    parse: (response) ->
        response.message

module.exports = MessageModel
