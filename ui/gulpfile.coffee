gulp = require("gulp")
gulpLoadPlugins = require("gulp-load-plugins")
plugins = gulpLoadPlugins()
run = require('run-sequence')

dist = 'distribution/'
staticSrc = ['images/*', 'statics/*']
hbsSrc = 'templates/**/*.hbs'
coffeeSrc = ['scripts/*.coffee', 'scripts/**/*.coffee']

gulp.task('default', ['watch'])

#####

gulp.task('build', ->
    run(
        'clean'
        [
            'copy:static'
            'copy:fonts'
            'styleguide'
            'styles:app'
            'scripts:app'
            # TODO: Run Codo
        ]
    )
)

gulp.task('watch', ['build'], ->
    gulp.watch(
        staticSrc
        ['copy:static']
    )
    gulp.watch(
        ['styles/*.styl', 'styles/**/*.styl']
        ['styles:app', 'styleguide']
    )
    gulp.watch(
        coffeeSrc.concat(hbsSrc)
        ['scripts:app']
    )
)

gulp.task('deploy', ->
    run(
        'clean'
        [
            'copy:static'
            'copy:fonts'
            'styleguide'
            'styles:app'
            'scripts:app'
            # TODO: Run Codo
        ]
        [
            'minify-css'
            'uglify'
        ]
    )
)

gulp.task('test', ->
    run(
        [
            'build'
            'scripts:test'
        ]
        'mocha-phantomjs'
    )
)

#####

gulp.task('clean', ->
    gulp.src(dist, {read: false})
        .pipe(plugins.clean())
)

gulp.task('copy:static', ->
    gulp.src(staticSrc)
        .pipe(gulp.dest(dist))
)

gulp.task('copy:fonts', ->
    gulp.src('node_modules/font-awesome/fonts/fontawesome-webfont.*')
        .pipe(gulp.dest(dist + 'fonts/'))
)

gulp.task('styles:app', ->
    gulp.src('styles/app.styl')
        .pipe(plugins.stylus({ set: ['include css'] }))
        .pipe(gulp.dest(dist))
)

gulp.task('styleguide', ->
    yms = require('ym-styleguide')
    fs = require('fs')
    yms.build('styles/', (html) ->
        fs.writeFile('templates/sections/styleguide/compiled.hbs', html)
    )
)

gulp.task('scripts:app', ->
    gulp.src('scripts/app.coffee', { read: false })
        .pipe(plugins.browserify({
            transform: ['coffeeify', 'hbsfy']
            extensions: ['.js', '.coffee', '.hbs']
            debug: true
        }))
        .pipe(plugins.rename('app.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:test', ->
    gulp.src(coffeeSrc)
        .pipe(plugins.coffeelint())
        .pipe(plugins.coffeelint.reporter('fail'))
)

gulp.task('minify-css', ->
    gulp.src(dist + 'app.css')
        .pipe(plugins.minifyCss())
        .pipe(gulp.dest(dist))
)

gulp.task('uglify', ->
    gulp.src(dist + 'app.js')
        .pipe(plugins.uglify())
        .pipe(gulp.dest(dist))
)

gulp.task('mocha-phantomjs', ->
    # plugins.mochaPhantomjs()
)
