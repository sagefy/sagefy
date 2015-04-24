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

################################################################################
### Configuration ##############################################################
################################################################################

dist = 'distribution/'
staticSrc = ['images/*', 'statics/*']
hbsSrc = 'templates/**/*.hbs'
coffeeSrc = ['scripts/*.coffee', 'scripts/**/*.coffee']
testSrc = ['test/*.coffee', 'test/**/*.coffee']

################################################################################
### Main Tasks #################################################################
################################################################################

gulp.task('default', ['watch'])

gulp.task('watch', (done) ->
    sequence('clean', [
        'static:watch'
        'styles:watch'
        'scripts:watch'
    ], done)
)

gulp.task('deploy', (done) ->
    sequence('clean', [
        'static:build'
        'styles:compress'
        'scripts:compress'
    ], done)
)

gulp.task('test', [
    'scripts:test:lint'
    'scripts:test:run'
])

################################################################################
### Subtasks ###################################################################
################################################################################

gulp.task('clean', (done) ->
    del(dist, (err, files) ->
        return console.error(err) if err
        done()
    )
)

gulp.task('static:build', ->
    gulp.src(staticSrc)
        .pipe(gulp.dest(dist))
    gulp.src('node_modules/font-awesome/fonts/fontawesome-webfont.woff')
        .pipe(gulp.dest(dist))
)

gulp.task('static:watch', ['static:build'], ->
    gulp.watch(
        staticSrc
        ['static:build']
    )
)

gulp.task('styles:build', ->
    gulp.src('styles/index.styl')
        .pipe(stylus({
            'include css': true
            errors: true
            use: husl()
        }))
        .pipe(gulp.dest(dist))
)

gulp.task('styles:build:doc', ->
    gulp.src('../gh-pages/index.styl')
        .pipe(stylus({
            'include css': true
            errors: true
            use: husl()
        }))
        .pipe(gulp.dest('../gh-pages/'))
)

gulp.task('styles:doc', (done) ->
    yms = require('ym-styleguide')
    fs = require('fs')
    yms.build('styles/', (html) ->
        coffee = 'module.exports="""\n' + html + '\n"""\n'
        fs.writeFileSync('scripts/templates/pages/compiled.coffee', coffee)
        done()
    )
)

gulp.task('styles:compress', ['styles:build'], ->
    gulp.src(dist + 'index.css')
        .pipe(minifyCss())
        .pipe(gulp.dest(dist))
)

gulp.task('styles:watch', ['styles:build', 'styles:build:doc'], ->
    gulp.watch(
        ['styles/*.styl', 'styles/**/*.styl']
        ['styles:build', 'styles:build:doc', 'scripts:build']
    )
)

gulp.task('content', ->
    gulp.src('../content/*.yml')
        .pipe(yaml())
        .pipe(gulp.dest('./scripts/content/'))
)

gulp.task('scripts:build', ['styles:doc', 'content'], ->
    browserify({
        entries: ['./scripts/index.coffee']
        extensions: ['.js', '.coffee']
        debug: true
    })
        .bundle()
        .pipe(source('index.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:watch', ['scripts:build'], ->
    bundle = watchify(browserify({
        entries: ['./scripts/index.coffee']
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
            'Finished', gutil.colors.cyan("'scripts:watch'"),
            'after', gutil.colors.magenta(endTime)
        )
    bundle.on('update', rebundle)
    return rebundle()
)

gulp.task('scripts:compress', ['scripts:build'], ->
    gulp.src(dist + 'index.js')
        .pipe(uglify())
        .pipe(gulp.dest(dist))
)

gulp.task('scripts:test:build', ['styles:doc', 'content'], ->
    gulp.src([
        'node_modules/mocha/mocha.css'
        'node_modules/mocha/mocha.js'
    ])
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

gulp.task('scripts:test:lint', ->
    src = coffeeSrc
        .concat(testSrc)
        .concat(['!./scripts/templates/pages/compiled.coffee'])
    gulp.src(src)
        .pipe(coffeelint())
        .pipe(coffeelint.reporter('fail'))
)

gulp.task('scripts:test:run', ['content'], (done) ->
    mocha = new Mocha({
        reporter: 'min'
        compilers: 'coffee:coffee-script/register'
    })
    mocha.addFile('test/index.coffee')
    mocha.run(done)
)
