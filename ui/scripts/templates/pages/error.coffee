module.exports = (data) ->
    html = "<h1>#{data.code}</h1>"
    if data.message
        html += "<p>#{data.message}"
    return html
