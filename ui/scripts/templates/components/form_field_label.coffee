c = require('../../modules/content').get

module.exports = (data) ->
    required = data.validations?.required
    html = "<label for=\"#{data.name}\">"
    html += data.label or ''
    if data.type isnt 'message'
        kind = if required then c('required') else c('optional')
        html += """
        <span class="#{if required then "required" else "optional"}">
            #{kind}
        </span>
        """
    return html + '</label>'
