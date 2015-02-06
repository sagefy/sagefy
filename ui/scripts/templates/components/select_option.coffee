module.exports = (data) ->
    return """
    <li>
        <label>
            <input type="#{if data.chooseMultiple then 'radio' else 'checkbox'}"
                   value="#{data.value or ''}"
                   name="#{data.name}">
               #{data.label}
        </label>
    </li>
    """
