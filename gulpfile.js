const { task, src, dest, series, watch } = require("gulp");
const sass = require("gulp-sass");
const cleanCSS = require("gulp-clean-css");

//convert base.scss to css and minify
task("base", (done) => {
  src("TourDay/static/sass/base.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/css/"));

  done();
});

// convert croppie.scss to css and minify
task("croppie", (done) => {
  src("TourDay/static/sass/croppie.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/css/"));

  done();
});

// convert layout.scss to css and minify
task("layout", (done) => {
  src("TourDay/static/sass/layout.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/css/"));

  done();
});

// convert event.scss to css and minify
task("event", (done) => {
  src("TourDay/static/event/sass/event.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/event/css/"));

  done();
});

// convert dashboard.scss to css and minify
task("dashboard", (done) => {
  src("TourDay/static/event/sass/dashboard.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/event/css/"));

  done();
});

// convert map.scss to css and minify
task("map", (done) => {
  src("TourDay/static/profile/sass/map.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/profile/css/"));

  done();
});

// convert portfolio.scss to css and minify
task("portfolio", (done) => {
  src("TourDay/static/profile/sass/portfolio.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/profile/css/"));

  done();
});

// convert profile.scss to css and minify
task("profile", (done) => {
  src("TourDay/static/profile/sass/profile.scss")
    .pipe(sass().on("error", sass.logError))
    .pipe(cleanCSS())
    .pipe(dest("TourDay/static/profile/css/"));

  done();
});

task("watch", function () {
  watch("TourDay/static/sass/base.scss", series("base"));
  watch("TourDay/static/sass/croppie.scss", series("croppie"));
  watch("TourDay/static/sass/layout.scss", series("layout"));
  watch("TourDay/static/event/sass/event.scss", series("event"));
  watch("TourDay/static/event/sass/dashboard.scss", series("dashboard"));
  watch("TourDay/static/profile/sass/map.scss", series("map"));
  watch("TourDay/static/profile/sass/portfolio.scss", series("portfolio"));
  watch("TourDay/static/profile/sass/profile.scss", series("profile"));
});

task("default", (done) => {
  series("base");
  series("croppie");
  series("layout");
  series("event");
  series("dashboard");
  series("map");
  series("portfolio");
  series("profile");
  done();
});
