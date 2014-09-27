module.exports = (data) ->
    html = """
    <div class="form-field form-field--#{data.type}} form-field--#{data.name}">
        <label for="#{data.name}">
            #{title}
            <span class="#{if data.required then "required" else "optional"}">
                #{if data.required then "Required" else "Optional"}
            </span>
        </label>
    """

    html += switch data.type
        when 'text', 'email', 'password'
            """
            <input
                id="#{data.name}"
                name="#{data.name}"
                placeholder="#{data.placeholder}"
                type="#{data.type}"
            >
            """

    if data.description
        html += """
            <p class="form-field__description">#{data.description}</p>
        """

    return html + "</div>"
