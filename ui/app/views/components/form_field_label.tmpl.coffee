c = require('../../modules/content').get
requiredFn = require('../../modules/validations').required

module.exports = (data) ->
    isRequired = requiredFn in data.validations or []
    html = "<label for=\"#{data.name}\">"
    html += data.label or ''
    if data.type isnt 'message'
        kind = if isRequired then c('required') else c('optional')
        html += """
        <span class="#{if isRequired then "required" else "optional"}">
            #{kind}
        </span>
        """
    return html + '</label>'
