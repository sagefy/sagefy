module.exports = (data) ->
    return """
    <button type="submit">
        <i class="fa fa-#{data.icon}"></i>
        #{data.title}
    </button>
    """
