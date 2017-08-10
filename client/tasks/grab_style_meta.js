/* eslint-disable import/no-extraneous-dependencies,quotes */
const glob = require('glob')
const fs = require('fs')
const yaml = require('js-yaml')
// const markdown = require('marked')

// Given a string, capitalize the first letter
/* const ucFirst = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1)
} */

const build = (g, fn) => {
    const data = {}
    glob(g)
        .on('match', (path) => {
            const contents = fs.readFileSync(path, 'utf-8')
            ;(contents.match(/---(?!---)((.|\n)*?)---/g) || [])
                .filter(el => /---/.test(el))
                .map(el => el.replace(/---/g, ''))
                .forEach((y) => {
                    y = yaml.load(y)
                    // y.description = markdown(y.description)
                    data[y.title] = y
                })
        })
        .on('end', () => fn(data))
}

module.exports = build
