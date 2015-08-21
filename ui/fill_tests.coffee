# Write a test file for every script file.

glob = require('glob')
fs = require('fs')
mkdirp = require('mkdirp')

module.exports = ->
    glob('app/**/*.coffee').on('match', (file) ->
        file = file.replace('app/', 'test/')
        fs.readFile(file, (err, data) ->
            return if not err
            name = file.split('/').pop().replace('.coffee', '')
            mkdirp(file.split('/').slice(0, -1).join('/'), ->
                fs.writeFile(file, """
                describe('#{name}', ->
                    it.skip('needs tests', ->

                    )
                )

                """)
            )
        )
    )
