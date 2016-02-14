gulp = require('gulp')
gutil = require('gulp-util')
run = require('run-sequence')
browserify = require('browserify')
watchify = require('watchify')
source = require('vinyl-source-stream')
prettyHrtime = require('pretty-hrtime')
sequence = require('run-sequence')
rimraf = require('rimraf')
stylus = require('stylus')
husl = require('husl')
minifyCss = require('gulp-minify-css')
yaml = require('gulp-yaml')
uglify = require('gulp-uglify')
coffeelint = require('gulp-coffeelint')
Mocha = require('mocha')
mkdirp = require('mkdirp')

fillTests = require('./fill_tests')
grabStyleMeta = require('./grab_style_meta')

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
        'rewrite html'
        'copy fonts'
        'watch styles'
        'watch scripts'
    ], done)
)

gulp.task('build', ['deploy'])
gulp.task('deploy', (done) ->
    sequence('clean', [
        'rewrite html'
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
    rimraf(dist, done)
)

gulp.task('copy statics', ->
    gulp.src(staticSrc)
        .pipe(gulp.dest(dist))
)

gulp.task('rewrite html', ['copy statics'], (done) ->
    file = dist + 'index.html'
    require('fs').readFile(file, 'utf8', (err, str) ->
        throw new Error(err) if(err)
        str = str.replace(/___/g, Date.now())
        require('fs').writeFile(file, str, (err) ->
            done()
        )
    )
)

gulp.task('copy fonts', ->
    gulp.src('node_modules/font-awesome/fonts/fontawesome-webfont.woff')
        .pipe(gulp.dest(dist))
)

gulp.task('watch statics', ['copy statics'], ->
    gulp.watch(
        staticSrc
        ['rewrite html']
    )
)

stylus2css = (from, to, done) ->
    require('fs').readFile(from, 'utf8', (err, styl) ->
        stylus(styl)
            .set('filename', from)
            .set('include css', true)
            .define('huslp', (h, s, l, a) ->
                [r, g, b] = husl.p.toRGB(h.val, s.val, l.val)
                a ?= 1
                return new stylus.nodes.RGBA(r * 255, g * 255, b * 255, a)
            )
            .render((err, css) ->
                throw err if err
                mkdirp(to.split('/').slice(0, -1).join('/'), ->
                    require('fs').writeFile(to, css, done)
                )
            )
    )

gulp.task('build styles', (done) ->
    from = './app/index.styl'
    to = dist + 'index.css'
    stylus2css(from, to, done)
)

gulp.task('build styleguide', (done) ->
    fs = require('fs')
    grabStyleMeta('./**/*.styl', (data) ->
        content = JSON.stringify(data)
        fs.writeFile(
            './app/views/pages/styleguide.data.json'
            content
            done
        )
    )
)

gulp.task('compress styles', ['build styles'], ->
    gulp.src(dist + 'index.css')
        .pipe(minifyCss())
        .pipe(gulp.dest(dist))
)

gulp.task('watch styles', ['build styles'], ->
    gulp.watch(
        ['app/**/*.styl']
        ['build styles', 'build scripts']
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
