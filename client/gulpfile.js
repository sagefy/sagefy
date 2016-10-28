/* eslint-disable import/no-extraneous-dependencies */
const gulp = require('gulp')
const gutil = require('gulp-util')
const browserify = require('browserify')
const watchify = require('watchify')
const source = require('vinyl-source-stream')
const prettyHrtime = require('pretty-hrtime')
const stylus = require('stylus')
const husl = require('husl')
const mkdirp = require('mkdirp')
const fs = require('fs')

const fillTests = require('./fill_tests')
const grabStyleMeta = require('./grab_style_meta')

/* #############################################################################
### Configuration ##############################################################
############################################################################# */

const dist = 'distribution/'
const staticSrc = ['app/images/*', 'app/*.{html,txt,ico}']

/* #############################################################################
### Subtasks ###################################################################
############################################################################# */

gulp.task('rewrite html', (done) => {
    const file = dist + 'index.html'
    fs.readFile(file, 'utf8', (err, str) => {
        if(err) { throw new Error(err) }
        str = str.replace(/___/g, Date.now())
        fs.writeFile(file, str, () =>
            done()
        )
    })
})

gulp.task('watch statics', () =>
    gulp.watch(
        staticSrc,
        ['rewrite html']
    )
)

const stylus2css = (from, to, done) =>
    fs.readFile(from, 'utf8', (err, styl) =>
        stylus(styl)
            .set('filename', from)
            .set('include css', true)
            .define('huslp', (h, s, l, a) => {  // eslint-disable-line max-params, max-len
                const [r, g, b] = husl.p.toRGB(h.val, s.val, l.val)
                a = a || 1
                return new stylus.nodes.RGBA(r * 255, g * 255, b * 255, a)
            })
            .render((err, css) => {
                if (err) { throw err }
                mkdirp(to.split('/').slice(0, -1).join('/'), () =>
                    fs.writeFile(to, css, done)
                )
            })
    )

gulp.task('build styles', (done) => {
    const from = './app/index.styl'
    const to = dist + 'index.css'
    stylus2css(from, to, done)
})

gulp.task('build styleguide', (done) => {
    grabStyleMeta('./**/*.styl', (data) => {
        const content = JSON.stringify(data)
        fs.writeFile(
            './app/views/pages/styleguide.data.json',
            content,
            done
        )
    })
})

gulp.task('watch styles', () =>
    gulp.watch(
        ['app/**/*.styl'],
        ['build styles', 'build scripts']
    )
)

gulp.task('build scripts', () =>
    browserify({
        entries: ['./app/index.js'],
        debug: true,
    })
        .bundle()
        .pipe(source('index.js'))
        .pipe(gulp.dest(dist))
)

gulp.task('watch scripts', () => {
    const bundle = watchify(browserify({
        entries: ['./app/index.js'],
        debug: true,
        cache: {},
        packageCache: {},
        fullPaths: true,
    }))
    const rebundle = () => {
        const startTime = process.hrtime()
        bundle
            .bundle()
            .pipe(source('index.js'))
            .pipe(gulp.dest(dist))
        const endTime = prettyHrtime(process.hrtime(startTime))
        gutil.log(
            'Finished', gutil.colors.cyan("'watch scripts'"),
            'after', gutil.colors.magenta(endTime)
        )
    }
    bundle.on('update', rebundle)
    return rebundle()
})

gulp.task('build test scripts', () => {
    return browserify({
        entries: ['./test/index.js'],
        debug: true,
    })
        .bundle()
        .pipe(source('test.js'))
        .pipe(gulp.dest(dist))
})

gulp.task('fill tests', (done) =>
    fillTests(done)
)
