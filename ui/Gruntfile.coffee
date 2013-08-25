LIVERELOAD_PORT = 35729
lrSnippet = require('connect-livereload')(port: LIVERELOAD_PORT)

mountFolder = (connect, dir) ->
    connect.static(require('path').resolve(dir))

###
TODOS:
[ ] Add testing
[ ] Improve requires for development
[ ] Build
###

module.exports = (grunt) ->

    require('load-grunt-tasks')(grunt)

    grunt.initConfig
        clean:
            main:
                files:
                    src: ['tmp/']
            build:
                files:
                    src: ['distribution/']
        concurrent:
            main: [
                'copy:main'
                'handlebars:main'
                'stylus:main'
                'coffee:main'
            ]
            build: [
                'copy:build'
                'handlebars:build'
                'stylus:build'
                'coffee:build'
            ]
        copy:
            main:
                files: [
                    expand: true
                    flatten: true
                    dest: 'tmp'
                    src: [
                        'images/**'
                        'statics/**'
                    ]
                ]
            build:
                files: [
                    expand: true
                    flatten: true
                    dest: 'distribution/'
                    src: [
                        'images'
                        'statics'
                    ]
                ]
        handlebars:
            options:
                namespace: 'HBS'
                processName: (file) ->
                    file.replace('templates/', '').replace('.hbs', '')
                partialsUseNamespace: true
                partialRegex: /^_/
                processPartialName: (file) ->
                    file.replace('templates/', '').replace('.hbs', '')
            main:
                files:
                    'tmp/templates.js': 'templates/**/*.hbs'
            build:
                files:
                    'distribution/templates.js': 'templates/**/*.hbs'
        stylus:
            main:
                options:
                    compress: false
                files:
                    'tmp/app.css': 'stylesheets/app.styl'
            build:
                options:
                    compress: true
                files:
                    'distribution/app.css': 'stylesheets/app.styl'
        coffee:
            main:
                files: [
                    expand: true
                    cwd: 'scripts/'
                    src: ['*.coffee', '**/*.coffee']
                    dest: 'tmp'
                    ext: '.js'
                ]
            build:
                files: [
                    expand: true
                    cwd: 'scripts/'
                    src: ['*.coffee', '**/*.coffee']
                    dest: 'distribution'
                    ext: '.js'
                ]
        connect:
            options:
                port: 9000
                hostname: 'localhost'
            livereload:
                options:
                    middleware: (connect) ->
                        [
                            lrSnippet
                            mountFolder(connect, 'bower_components')
                            mountFolder(connect, 'tmp')
                        ]
        open:
            server:
                path: 'http://localhost:<%= connect.options.port %>'
        watch:
            coffee:
                files: ['scripts/*.coffee', 'scripts/**/*.coffee']
                tasks: ['coffee:main']
            handlebars:
                files: ['templates/**/*.hbs']
                tasks: ['handlebars:main']
            stylus:
                files: ['stylesheets/*.styl', 'stylesheets/**/*.styl']
                tasks: ['stylus:main']
            copy:
                files: [
                    'images/*'
                    'images/**/*'
                    'statics/*'
                    'statics/**/*'
                ]
                tasks: ['copy:main']
            livereload:
                options:
                    livereload: LIVERELOAD_PORT
                files: [
                    'scripts/*.coffee'
                    'scripts/**/*.coffee'
                    'stylesheets/*.styl'
                    'stylesheets/**/*.styl'
                    'templates/*.hbs'
                    'templates/**/*.hbs'
                    'images/*'
                    'images/**/*'
                    'statics/*'
                    'statics/**/*'
                ]
        requirejs:
            build:
                options:
                    baseUrl: '/distribution'
                    optimize: 'none'
                    preserveLicenseComments: 'true'
                    useStrict: true
                    wrap: true
                    out: '/distribution'
        uglify:
            build:
                files:
                    'distribution/app.js': ['distribution/app.js']

    grunt.registerTask 'run', [
        'clean:main'
        'concurrent:main'
        'connect:livereload'
        'open'
        'watch'
    ]

    grunt.registerTask 'test', [
        'clean:main'
        'concurrent:main'
        'connect:livereload'
        # TODO: run test suites
    ]

    grunt.registerTask 'build', [
        'clean:build'
        'concurrent:build'
        'requirejs:build'
        'uglify:build'
    ]

    grunt.registerTask 'default', ['run']

