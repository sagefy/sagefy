// Write a test file for every script file.
/* eslint-disable import/no-extraneous-dependencies,quotes */

const glob = require('glob')
const fs = require('fs')
const mkdirp = require('mkdirp')

const fillTests = () =>
    glob('app/**/*.js').on('match', (file) => {
        const testFile = file.replace('app/', 'test/')
        fs.readFile(testFile, (err) => {
            if(err) { return }
            const testPath = file.split('/').slice(0, -1).join('/')
            const len = file.split('/').length
            const originalFile = ((new Array(len)).join('../') + file)
                .replace('.js', '')
            const contextName = file.split('/')
                .pop()
                .toLowerCase()
                .replace('.js', '')
                .replace(/[_\.]/g, ' ')
            const moduleName = file.split('/')
                .pop()
                .toLowerCase()
                .replace('.js', '')
                .replace(/[_.]([a-z])/g, g => g[1].toUpperCase())
            mkdirp(testPath, () => {
                fs.writeFile(testFile, [
                    `${moduleName} = require('${originalFile}')`,
                    "const {expect} = require('chai')",
                    `describe('${contextName}', () => {`,
                    "    it.skip('needs tests', () =>",
                    "        expect(false).to.be.true",
                    "    })",
                    "})",
                ].join(''))
            })
        })
    })

if (require.main === module) {
    fillTests()
}

module.exports = fillTests
