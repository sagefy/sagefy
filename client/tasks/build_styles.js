/* eslint-disable import/no-extraneous-dependencies */
const fs = require('fs')
const stylus = require('stylus')
const husl = require('husl')
const mkdirp = require('mkdirp')

const dist = 'distribution/'

const stylus2css = (from, to, done) =>
    fs.readFile(from, 'utf8', (err, styl) =>
        stylus(styl)
            .set('filename', from)
            .set('include css', true)
            .define('huslp', (h, s, l, a) => {  // eslint-disable-line max-params, max-len
                const [r, g, b] = husl.p.toRGB(h.val, s.val, l.val)
                a = a || 1
                return new stylus.nodes.RGBA(r * 255, g * 255, b * 255, a)
            })
            .render((err, css) => {
                if (err) { throw err }
                mkdirp(to.split('/').slice(0, -1).join('/'), () =>
                    fs.writeFile(to, css, done)
                )
            })
    )

const from = './app/index.styl'
const to = dist + 'index.css'
stylus2css(from, to)
