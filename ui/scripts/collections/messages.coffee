Backbone = require('backbone')
MessageModel = require('../models/message')

class MessagesCollection extends Backbone.UsersCollection
    model: MessageModel

module.exports = MessagesCollection
