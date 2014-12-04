# TODO: break this up

module.exports = (data) ->
    if data.type is 'submit'
        return """
        <button type="submit">
            <i class="fa fa-#{data.icon}"></i>
            #{data.label}
        </button>
        """

    if data.type is 'message'
        return """
        <div class="form-field">
            <label>#{data.title}</label>
            <p class="form-field__description">#{data.description}</p>
        </div>
        """

    required = data.validations.required

    # TODO: move copy to content directory  Required/Optional
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
                value="#{data.value or ''}"
            >
            """

    if data.description
        html += """
            <p class="form-field__description">#{data.description}</p>
        """

    return html + "</div>"
