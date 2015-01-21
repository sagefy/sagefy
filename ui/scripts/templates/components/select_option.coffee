module.exports = (data) ->
    return """
    <li>
        <input type="#{if data.chooseMultiple then 'radio' else 'checkbox'}"
               value="#{data.value or ''}"
               id="#{data.slug}"
               name="#{data.slug}">
        <label for="#{data.slug}">#{data.name}</label>
    </li>
    """
