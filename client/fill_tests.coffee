# Write a test file for every script file.

glob = require('glob')
fs = require('fs')
mkdirp = require('mkdirp')

module.exports = ->
    glob('app/**/*.coffee').on('match', (file) ->
        testFile = file.replace('app/', 'test/')

        fs.readFile(testFile, (err, data) ->
            return unless err

            testPath = file.split('/').slice(0, -1).join('/')

            len = file.split('/').length
            originalFile = (new Array(len)).join('../') + file

            contextName = file.split('/')
                .pop()
                .toLowerCase()
                .replace('.coffee', '')
                .replace(/[_\.]/g, ' ')

            moduleName = file.split('/')
                .pop()
                .toLowerCase()
                .replace('.coffee', '')
                .replace(/[_.]([a-z])/g, (g) -> g[1].toUpperCase())

            mkdirp(testPath, ->
                fs.writeFile(testFile, """
                    #{moduleName} = require('#{originalFile}')
                    expect = require('chai').expect

                    describe('#{contextName}', ->
                        it.skip('needs tests', ->
                            expect(false).to.be.true
                        )
                    )

                """)
            )
        )
    )
