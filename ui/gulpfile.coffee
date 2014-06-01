gulp = require("gulp")
gutil = require('gulp-util')
gulpLoadPlugins = require("gulp-load-plugins")
plugins = gulpLoadPlugins()
run = require('run-sequence')
browserify = require('browserify')
watchify = require('watchify')
source = require('vinyl-source-stream')
prettyHrtime = require('pretty-hrtime')
_ = require('underscore')

dist = 'distribution/'
staticSrc = ['images/*', 'statics/*']
hbsSrc = 'templates/**/*.hbs'
coffeeSrc = ['scripts/*.coffee', 'scripts/**/*.coffee']
testSrc = ['tests/*.coffee', 'tests/**/*.coffee']

gulp.task('default', ['watch'])

#####

gulp.task('watch', ->
    run(
        'clean'
        [
            'static:build'
            'styles:build'
            'scripts:build'
        ]
        [
            'static:watch'
            'styles:watch'
            'scripts:watch'
        ]
    )
)

gulp.task('deploy', ->
    run(
        'clean'
        [
            'static:build'
            'styles:build'
            'scripts:build'
        ]
        [
            'styles:compress'
            'scripts:compress'
        ]
    )
)

gulp.task('test', ->
    run(
        'clean'
        [
            'static:build'
            'styles:build'
            'scripts:test:lint'
            'scripts:test:build'
        ]
        'scripts:test:run'
    )
)

#####

gulp.task('clean', ->
    gulp.src(dist, {read: false})
        .pipe(plugins.clean())
)

gulp.task('static:build', ->
    gulp.src(staticSrc)
        .pipe(gulp.dest(dist))
    gulp.src('node_modules/font-awesome/fonts/fontawesome-webfont.*')
        .pipe(gulp.dest(dist + 'fonts/'))
)

gulp.task('static:watch', ->
    gulp.watch(
        staticSrc
        ['static:build']
    )
)

gulp.task('styles:build', ->
    gulp.src('styles/app.styl')
        .pipe(plugins.stylus({set: ['include css']}))
        .pipe(gulp.dest(dist))
    run('styles:doc')
)

gulp.task('styles:doc', ->
    yms = require('ym-styleguide')
    fs = require('fs')
    yms.build('styles/', (html) ->
        fs.writeFile('templates/sections/styleguide/compiled.hbs', html)
    )
)

gulp.task('styles:compress', ->
    gulp.src(dist + 'app.css')
        .pipe(plugins.minifyCss())
        .pipe(gulp.dest(dist))
)

gulp.task('styles:watch', ->
    gulp.watch(
        ['styles/*.styl', 'styles/**/*.styl']
        ['styles:build']
    )
)

browserifyConfig = {
    entries: ['./scripts/app.coffee']
    extensions: ['.js', '.coffee', '.hbs']
    debug: true
}

gulp.task('scripts:build', ->
    browserify(browserifyConfig)
        .bundle()
        .pipe(source('app.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:watch', ->
    bundle = watchify(browserifyConfig)
    rebundle = ->
        startTime = process.hrtime()
        bundle
            .bundle()
            .pipe(source('app.js'))
            .pipe(gulp.dest(dist))
        endTime = prettyHrtime(process.hrtime(startTime))
        gutil.log(
            'Finished', gutil.colors.cyan("'scripts:watch'"),
            'after', gutil.colors.magenta(endTime)
        )
    bundle.on('update', rebundle)
    return rebundle()
)

gulp.task('scripts:compress', ->
    gulp.src(dist + 'app.js')
        .pipe(plugins.uglify())
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:test:build', ->
    gulp.src([
        'node_modules/mocha/mocha.css'
        'node_modules/mocha/mocha.js'
        'node_modules/chai/chai.js'
        'node_modules/jquery/dist/jquery.js'
        'node_modules/chai-jquery/chai-jquery.js'
    ])
        .pipe(gulp.dest(dist))

    config = _.extend({}, browserifyConfig)
    config.entries = ['./tests/test.coffee']

    browserify(config)
        .bundle()
        .pipe(source('test.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:test:lint', ->
    gulp.src(coffeeSrc.concat(testSrc))
        .pipe(plugins.coffeelint())
        .pipe(plugins.coffeelint.reporter())
        # send reporter('fail') to fail out
)

gulp.task('scripts:test:run', ->
    gulp.src(dist + 'test.html')
        .pipe(plugins.mochaPhantomjs({reporter: 'spec'}))
)
