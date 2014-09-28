module.exports = (data) ->
    if data.type is 'submit'
        return """
        <button type="submit">
            <i class="fa fa-#{data.icon}"></i>
            #{data.label}
        </button>
        """

    required = data.validations.required

    html = """
    <div class="form-field form-field--#{data.type}} form-field--#{data.name}">
        <label for="#{data.name}">
            #{data.title}
            <span class="#{if required then "required" else "optional"}">
                #{if required then "Required" else "Optional"}
            </span>
        </label>
    """

    html += switch data.type
        when 'text', 'email', 'password'
            """
            <input
                id="#{data.name}"
                name="#{data.name}"
                placeholder="#{data.placeholder or ''}"
                type="#{data.type}"
            >
            """

    if data.description
        html += """
            <p class="form-field__description">#{data.description}</p>
        """

    return html + "</div>"
