Backbone = require('backbone')
MessageModel = require('../models/message')

class MessagesCollection extends Backbone.Collection
    model: MessageModel

module.exports = MessagesCollection
