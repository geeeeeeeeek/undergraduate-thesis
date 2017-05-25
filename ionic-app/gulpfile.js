var gulp = require('gulp')
var concat = require('gulp-concat')
var sass = require('gulp-sass')
var minifyCss = require('gulp-minify-css')
var rename = require('gulp-rename')
var sourcemaps = require('gulp-sourcemaps')
var babel = require('gulp-babel')
var ngAnnotate = require('gulp-ng-annotate')
var uglify = require('gulp-uglify')

gulp.task('default', ['sass', 'scripts'])

gulp.task('serve:before', ['watch'])

gulp.task('sass', function (done) {
  gulp.src('./scss/ionic.app.scss')
        .pipe(sourcemaps.init())
        .pipe(sass({
          errLogToConsole: true
        }))
        .pipe(minifyCss({
          keepSpecialComments: 0
        }))
        .pipe(rename({extname: '.min.css'}))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./www/assets/css/'))
        .on('end', done)
})

gulp.task('scripts', function () {
  return gulp.src(['www/js/*.js', 'www/js/**/*.js'])
        .pipe(sourcemaps.init())
        .pipe(babel({presets: ['es2015']}))
        .pipe(ngAnnotate())
        .pipe(concat('main.min.js'))
        .pipe(uglify())
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./www/assets/script/'))
})

gulp.task('watch', ['default'], function () {
  gulp.watch(['./scss/**/*.scss'], ['sass'])
  gulp.watch(['www/js/*.js', 'www/js/**/*.js'], ['scripts'])
})
