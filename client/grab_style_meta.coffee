glob = require('glob')
fs = require('fs')
yaml = require('js-yaml')
markdown = require('marked')

# Given a string, capitalize the first letter
ucFirst = (string) ->
    return string.charAt(0).toUpperCase() + string.slice(1)

build = (g, fn) ->
    data = {}
    glob(g)
        .on('match', (path) ->
            contents = fs.readFileSync(path, 'utf-8')
            (contents.match(/---(?!---)((.|\n)*?)---/g) or [])
                .filter((el) -> /---/.test(el))
                .map((el) -> el.replace(/---/g, ''))
                .forEach((y) ->
                    y = yaml.load(y)
                    # y.description = markdown(y.description)
                    data[y.title] = y
                )
        )
        .on('end', ->
            fn(data)
        )

module.exports = build
