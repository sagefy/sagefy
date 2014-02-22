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
    gulp.watch staticSrc, ['copyStatic']
    gulp.watch hbsSrc, ['handlebars']
    gulp.watch ['stylesheets/*.styl', 'stylesheets/**/*.styl'], ['stylus']
    gulp.watch coffeeSrc, ['coffee']

gulp.task 'deploy', ['build'], ->
    # TODO: Compile Requires
    # TODO: Uglify and Compress Files

gulp.task 'test', ['build'], ->
    # TODO: Run test suites

#####

gulp.task 'build', ['clean'], ->
    gulp.run 'copyStatic', 'bower', 'handlebars', 'stylus', 'coffee'

gulp.task 'clean', ->
    gulp.src dist, read: false
        .pipe plugins.clean()

gulp.task 'copyStatic', ->
    gulp.src staticSrc
        .pipe gulp.dest dist

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
        .pipe plugins.stylus()
        .pipe gulp.dest dist

gulp.task 'coffee', ->
    gulp.src coffeeSrc
        .pipe plugins.coffee()
        .pipe gulp.dest dist
