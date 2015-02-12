module.exports = (data) ->
    return """
    <li>
        <label>
            <input type="#{if data.multiple then 'checkbox' else 'radio'}"
                   value="#{data.value or ''}"
                   name="#{data.name}">
               #{data.label}
        </label>
    </li>
    """
