gulp = require "gulp"
gulpLoadPlugins = require "gulp-load-tasks"
plugins = gulpLoadPlugins()

dist = 'distribution/'
staticSrc = ['images/*', 'statics/*']
hbsSrc = 'templates/**/*.hbs'
coffeeSrc = ['scripts/*.coffee', 'scripts/**/*.coffee']

gulp.task 'default', ['watch'], ->

#####

gulp.task 'watch', ['build'], ->
    gulp.watch(staticSrc, ['copyStatic'])
    gulp.watch(hbsSrc, ['handlebars'])
    gulp.watch(['stylesheets/*.styl', 'stylesheets/**/*.styl'], ['stylus', 'styleguide'])
    gulp.watch(coffeeSrc, ['coffee'])

gulp.task 'deploy', [
    'build'
    # TODO: Compile Requires
    # TODO: Uglify and Compress Files
    # TODO: Run KSS & JSDoc
]

gulp.task 'test', [
    'build'
    'testCoffee'
    # TODO: Run Mocha
]

#####

gulp.task 'build', ['clean'], ->
    gulp.run(
        'copyStatic',
        'copyFonts',
        'bower',
        'styleguide',
        'handlebars',
        'stylus',
        'coffee'
    )

gulp.task 'clean', ->
    gulp.src dist, read: false
        .pipe plugins.clean()

gulp.task 'copyStatic', ->
    gulp.src staticSrc
        .pipe gulp.dest dist

gulp.task('copyFonts', ->
    gulp.src('bower_components/fontawesome/fonts/fontawesome-webfont.*')
        .pipe(gulp.dest(dist + 'fonts/'))
)

gulp.task 'bower', ->
    plugins['bower-files']()
        .pipe gulp.dest dist + 'bower/'

gulp.task 'handlebars', ->
    gulp.src hbsSrc
        .pipe plugins.handlebars
            outputType: 'amd'
            wrapped: true
        .pipe gulp.dest dist + 'hbs/'

gulp.task 'stylus', ->
    gulp.src 'stylesheets/app.styl'
        .pipe plugins.stylus({ set: ['include css'] })
        .pipe gulp.dest dist

gulp.task 'styleguide', ->
    yms = require 'ym-styleguide'
    fs = require 'fs'
    yms.build 'stylesheets/', (html) ->
        fs.writeFile 'templates/sections/styleguide/compiled.hbs', html

gulp.task 'coffee', ->
    gulp.src coffeeSrc
        .pipe plugins.coffeelint()
        .pipe plugins.coffeelint.reporter('default')
        .pipe plugins.coffee()
        .pipe gulp.dest dist

gulp.task 'testCoffee', ->
    gulp.src coffeeSrc
        .pipe plugins.coffeelint()
        .pipe plugins.coffeelint.reporter('fail')
