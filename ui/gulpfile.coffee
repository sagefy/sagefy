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

gulp.task('watch', [
    'static:watch'
    'styles:watch'
    'scripts:watch'
])

gulp.task('deploy', [
    'static:build'
    'styles:compress'
    'scripts:compress'
])

gulp.task('test', [
    'scripts:test:lint'
    'scripts:test:run'
])

#####

gulp.task('clean', ->
    gulp.src(dist, {read: false})
        .pipe(plugins.clean())
)

gulp.task('static:build', ['clean'], ->
    gulp.src(staticSrc)
        .pipe(gulp.dest(dist))
    gulp.src('node_modules/font-awesome/fonts/fontawesome-webfont.*')
        .pipe(gulp.dest(dist + 'fonts/'))
)

gulp.task('static:watch', ['static:build'], ->
    gulp.watch(
        staticSrc
        ['static:build']
    )
)

gulp.task('styles:build', ['clean'], ->
    gulp.src('styles/app.styl')
        .pipe(plugins.stylus({
            'include css': true
            errors: true
        }))
        .pipe(gulp.dest(dist))
)

gulp.task('styles:doc', ['clean'], (done) ->
    yms = require('ym-styleguide')
    fs = require('fs')
    yms.build('styles/', (html) ->
        fs.writeFileSync('templates/sections/styleguide/compiled.hbs', html)
        done()
    )
)

gulp.task('styles:compress', ['styles:build'], ->
    gulp.src(dist + 'app.css')
        .pipe(plugins.minifyCss())
        .pipe(gulp.dest(dist))
)

gulp.task('styles:watch', ['styles:build'], ->
    gulp.watch(
        ['styles/*.styl', 'styles/**/*.styl']
        ['styles:build', 'scripts:build']
    )
)

browserifyConfig = {
    entries: ['./scripts/app.coffee']
    extensions: ['.js', '.coffee', '.hbs']
    debug: true
}

gulp.task('scripts:build', ['styles:doc'], ->
    browserify(browserifyConfig)
        .bundle()
        .pipe(source('app.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:watch', ['scripts:build'], ->
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

gulp.task('scripts:compress', ['scripts:build'], ->
    gulp.src(dist + 'app.js')
        .pipe(plugins.uglify())
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:test:build', ['styles:doc'], ->
    gulp.src([
        'node_modules/mocha/mocha.css'
        'node_modules/mocha/mocha.js'
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
        .pipe(plugins.coffeelint.reporter('fail'))
)

gulp.task('scripts:test:run', [
    'styles:build'
    'static:build'
    'scripts:test:build'
], ->
    gulp.src(dist + 'test.html')
        .pipe(plugins.mochaPhantomjs({reporter: 'spec'}))
)
