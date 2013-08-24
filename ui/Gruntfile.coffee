LIVERELOAD_PORT = 35729
lrSnippet = require('connect-livereload')({port: LIVERELOAD_PORT})

mountFolder = (connect, dir) ->
    connect.static(require('path').resolve(dir))

module.exports = (grunt) ->

    require('load-grunt-tasks')(grunt)

    grunt.initConfig
        watch:
            coffee:
                files: ['coffeescripts/**.coffee']
                tasks: ['coffee:main']
            ###
            tests:
                files: ['tests/**.coffee']
                tasks: ['coffee:test']
            ###
            stylus:
                files: ['stylesheets/**.styl']
                tasks: ['stylus:main']
            livereload:
                options:
                    livereload: LIVERELOAD_PORT
                    files: [
                        '*.html'
                        'coffeescripts/**.coffee'
                        'stylesheets/**.styl'
                        'images/**.{png,jpg,jepg,gif,webp,svg}'
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
                            mountFolder(connect, '.tmp')
                            mountFolder(connect, '.')
                        ]
            ###
            test:
                options:
                    middleware: (connect) ->
                        [
                            mountFolder(connect, '.tmp')
                            mountFolder(connect, 'test')
                            mountFolder(connect, '.')
                        ]
            ###
        open:
            server:
                path: 'http://localhost:<%= connect.options.port %>'
        ###
        clean:
            main:
                files:
                    src: [
                        # '.tmp',
                        # '*'
                    ]
        ###
        coffee:
            main:
                files: [
                    expand: true
                    cwd: '/coffeescripts'
                    src: '**.coffee'
                    # dest: '.tmp/coffee'
                    # ext: '.js'
                ]
            ###
            test:
                files: [
                    expand: true
                    cwd: '/tests'
                    src: '**.coffee'
                    dest: '.tmp/tests'
                    ext: '.js'
                ]
            ###
        stylus:
            main:
                options:
                    compress: false
                    # use: [require('husl')]
                files:
                    'distribution/styleguide.css': 'stylesheets/styleguide.styl'
        requirejs:
            main:
                options:
                    baseUrl: '/coffeescripts'
                    optimize: 'none'
                    preserveLicenseComments: 'true'
                    useStrict: true
                    wrap: true
        ###
        copy:
            main:
                files: [
                    expand: true
                    dot: true
                    cwd: '.',
                    dest: 'distribution',
                    src: [
                        '*.{ico.png,txt}'
                    ]
                ]
        ###
        concurrent:
            main: [
                'stylus:main'
                'coffee:main'
                # 'copy:main'
            ]
            ###
            test: [
                'stylus:main'
                'coffee:main'
                'copy:main'
            ]
            build: [
                'stylus:main'
                'coffee:main'
                'copy:main'
            ]
            ###

    grunt.registerTask 'run', (target) ->
        if target == 'main'
            grunt.task.run ['build', 'open', 'connect:main:keepalive']

        grunt.task.run [
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
        'mocha'
    ]

    ###
    grunt.registerTask 'build', [
        'clean'
        'concurrent:build'
        'requirejs'
        'concat'
        'cssmin'
        'uglify'
        'copy:main'
    ]
    ###

    grunt.registerTask 'default', ['run']