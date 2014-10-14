Collection = require('../framework/collection')

class NoticesCollection extends Collection
    url: '/api/notices/'

    parse: (response) ->
        return response.notices

module.exports = NoticesCollection
