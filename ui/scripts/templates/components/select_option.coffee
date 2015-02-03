module.exports = (data) ->
    return """
    <li>
        <input type="#{if data.chooseMultiple then 'radio' else 'checkbox'}"
               value="#{data.value or ''}"
               id="#{data.id}"
               name="#{data.name}">
        <label for="#{data.id}">#{data.title}</label>
    </li>
    """
