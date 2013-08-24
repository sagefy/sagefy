
module.exports = (grunt) ->

    grunt.loadNpmTasks 'grunt-contrib-coffee'

    grunt.initConfig
        coffee:
            config:
                files:
                    src: ['**/*.coffee']

    grunt.registerTask 'run', [
        'coffee'
    ]

    grunt.registerTask 'default', ['run']