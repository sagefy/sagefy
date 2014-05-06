Backbone = require('backbone')
MessageModel = require('../models/message')

module.exports = class MessagesCollection extends Backbone.UsersCollection
    model: MessageModel

