gulp = require "gulp"
coffee = require "gulp-coffee"
sass = require "gulp-sass"

targets = [
	"coffee"
	"sass"
]

gulp.task "default", targets

gulp.task "coffee", ->
	gulp.src "src/coffee/*.coffee"
		.pipe coffee()
		.pipe gulp.dest "launch_physics/static/js/"

gulp.task "sass", ->
	gulp.src "src/sass/*.scss"
		.pipe sass().on "error", sass.logError
		.pipe gulp.dest "launch_physics/static/css/"
