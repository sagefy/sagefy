gulp = require('gulp')
gutil = require('gulp-util')
run = require('run-sequence')
browserify = require('browserify')
watchify = require('watchify')
source = require('vinyl-source-stream')
prettyHrtime = require('pretty-hrtime')
sequence = require('run-sequence')
del = require('del')
stylus = require('gulp-stylus')
husl = require('husl-stylus')
minifyCss = require('gulp-minify-css')
yaml = require('gulp-yaml')
uglify = require('gulp-uglify')
coffeelint = require('gulp-coffeelint')
Mocha = require('mocha')

fillTests = require('./fill_tests')

################################################################################
### Configuration ##############################################################
################################################################################

dist = 'distribution/'
staticSrc = ['app/images/*', 'app/*.{html,txt,ico}']
coffeeSrc = ['app/**/*.coffee']
testSrc = ['test/**/*.coffee']

################################################################################
### Main Tasks #################################################################
################################################################################

gulp.task('default', ['watch'])
gulp.task('develop', ['watch'])
gulp.task('watch', (done) ->
    sequence('clean', [
        'watch statics'
        'copy fonts'
        'watch styles'
        'watch scripts'
    ], done)
)

gulp.task('build', ['deploy'])
gulp.task('deploy', (done) ->
    sequence('clean', [
        'copy statics'
        'copy fonts'
        'compress styles'
        'compress scripts'
    ], done)
)

gulp.task('test', (done) ->
    sequence('clean', [
        'lint scripts'
        'run tests'
    ], done)
)

################################################################################
### Subtasks ###################################################################
################################################################################

gulp.task('clean', (done) ->
    del(dist, (err, files) ->
        return console.error(err) if err
        done()
    )
)

gulp.task('copy statics', ->
    gulp.src(staticSrc)
        .pipe(gulp.dest(dist))
)

gulp.task('copy fonts', ->
    gulp.src('node_modules/font-awesome/fonts/fontawesome-webfont.woff')
        .pipe(gulp.dest(dist))
)

gulp.task('watch statics', ['copy statics'], ->
    gulp.watch(
        staticSrc
        ['copy statics']
    )
)

gulp.task('build styles', ->
    gulp.src('app/index.styl')
        .pipe(stylus({
            'include css': true
            errors: true
            use: husl()
        }))
        .pipe(gulp.dest(dist))
)

gulp.task('build styles for docs', ->
    gulp.src('../gh-pages/index.styl')
        .pipe(stylus({
            'include css': true
            errors: true
            use: husl()
        }))
        .pipe(gulp.dest('../gh-pages/'))
)

gulp.task('build styleguide', (done) ->
    yms = require('ym-styleguide')
    fs = require('fs')
    yms.build('app/', (html) ->
        coffee = 'module.exports="""\n' + html + '\n"""\n'
        fs.writeFileSync('app/views/pages/styleguide.compiled.coffee', coffee)
        done()
    )
)

gulp.task('compress styles', ['build styles'], ->
    gulp.src(dist + 'index.css')
        .pipe(minifyCss())
        .pipe(gulp.dest(dist))
)

gulp.task('watch styles', ['build styles', 'build styles for docs'], ->
    gulp.watch(
        ['app/**/*.styl']
        ['build styles', 'build styles for docs', 'build scripts']
    )
)

gulp.task('compile content', ->
    gulp.src('../content/*.yml')
        .pipe(yaml())
        .pipe(gulp.dest('./app/content/'))
)

gulp.task('build scripts', ['build styleguide', 'compile content'], ->
    browserify({
        entries: ['./app/index.coffee']
        extensions: ['.js', '.coffee']
        debug: true
    })
        .bundle()
        .pipe(source('index.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('watch scripts', ['build scripts'], ->
    bundle = watchify(browserify({
        entries: ['./app/index.coffee']
        extensions: ['.js', '.coffee']
        debug: true
        cache: {}
        packageCache: {}
        fullPaths: true
    }))
    rebundle = ->
        startTime = process.hrtime()
        bundle
            .bundle()
            .pipe(source('index.js'))
            .pipe(gulp.dest(dist))
        endTime = prettyHrtime(process.hrtime(startTime))
        gutil.log(
            'Finished', gutil.colors.cyan("'watch scripts'"),
            'after', gutil.colors.magenta(endTime)
        )
    bundle.on('update', rebundle)
    return rebundle()
)

gulp.task('compress scripts', ['build scripts'], ->
    gulp.src(dist + 'index.js')
        .pipe(uglify())
        .pipe(gulp.dest(dist))
)

gulp.task('build test scripts', ['build styleguide', 'compile content'], ->
    gulp.src(['node_modules/mocha/mocha.js'])
        .pipe(gulp.dest(dist))

    browserify({
        entries: ['./test/index.coffee']
        extensions: ['.js', '.coffee']
        debug: true
    })
        .bundle()
        .pipe(source('test.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('lint scripts', ->
    src = coffeeSrc
        .concat(testSrc)
        .concat(['!./app/views/pages/styleguide.compiled.coffee'])
    gulp.src(src)
        .pipe(coffeelint())
        .pipe(coffeelint.reporter('fail'))
)

gulp.task('run tests', ['build test scripts'], (done) ->
    mocha = new Mocha({
        reporter: 'min'
        compilers: 'coffee:coffee-script/register'
    })
    mocha.addFile('test/index.coffee')
    mocha.run(done)
)

gulp.task('fill tests', (done) ->
    fillTests(done)
)
