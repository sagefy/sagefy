timeAgo = require('../../modules/utilities').timeAgo

module.exports = (data) ->
    return """
        <span class="notice__when">#{timeAgo(data.created)}</span>
        #{data.body}
    """
