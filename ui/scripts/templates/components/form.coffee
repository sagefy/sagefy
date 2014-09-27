module.exports = (data) ->
    html = data.fields

    if data.presubmit
        html += "<p>#{presubmit}</p>"

    html += """
    <button type="submit">
        <i class="fa fa-#{data.submitIcon}"></i>
        #{data.submitLabel}
    </button>
    """

    return html
