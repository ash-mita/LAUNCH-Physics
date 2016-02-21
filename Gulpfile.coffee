gulp = require "gulp"
coffee = require "gulp-coffee"
jade = require "gulp-jade"
sass = require "gulp-sass"

targets = [
	"coffee"
	"jade"
	"sass"
]

gulp.task "default", targets

gulp.task "coffee", ->
	gulp.src "src/coffee/*.coffee"
		.pipe coffee()
		.pipe gulp.dest "launch_physics/static/js/"

gulp.task "jade", ->
	gulp.src "src/jade/*.jade"
		.pipe jade {}
		.pipe gulp.dest "launch_physics/templates/"

gulp.task "sass", ->
	gulp.src "src/sass/*.scss"
		.pipe sass().on "error", sass.logError
		.pipe gulp.dest "launch_physics/static/css/"
