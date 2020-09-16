const gulp = require("gulp");
const { task, src, dest, series, watch } = gulp;
const sass = require("gulp-sass");
const cleanCSS = require("gulp-clean-css");
const uglify = require("gulp-uglify-es").default;
const rename = require("gulp-rename");

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

// blog -> style.css minify
task("style", (done) => {
  src("TourDay/static/blog/css/style.css")
    .pipe(cleanCSS())
    .pipe(rename({ suffix: ".min" }))
    .pipe(dest("TourDay/static/blog/css/"));

  done();
});

// blog -> search.css minify
task("search", (done) => {
  src("TourDay/static/blog/css/search.css")
    .pipe(cleanCSS())
    .pipe(rename({ suffix: ".min" }))
    .pipe(dest("TourDay/static/blog/css/"));

  done();
});

// minify forget.js
task("forgetjs", (done) => {
  src("TourDay/static/_auth/js/forgetpassword.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/_auth/js-min"));
  done();
});

// minify login.js
task("loginjs", (done) => {
  src("TourDay/static/_auth/js/login.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/_auth/js-min"));
  done();
});

// minify reset.js
task("resetjs", (done) => {
  src("TourDay/static/_auth/js/resetpassword.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/_auth/js-min"));
  done();
});

// minify signup.js
task("signupjs", (done) => {
  src("TourDay/static/_auth/js/signup.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/_auth/js-min"));
  done();
});

// minify dashboard.js
task("dashboardjs", (done) => {
  src("TourDay/static/event/js/dashboard.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/event/js-min"));
  done();
});

// minify eventjs
task("eventjs", (done) => {
  src("TourDay/static/event/js/event.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/event/js-min"));
  done();
});

// minify mapjs
task("mapjs", (done) => {
  src("TourDay/static/profile/js/map.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/profile/js-min"));
  done();
});

// minify portfoliojs
task("portfoliojs", (done) => {
  src("TourDay/static/profile/js/portfolio.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/profile/js-min"));
  done();
});

// minify profilejs
task("profilejs", (done) => {
  src("TourDay/static/profile/js/profile.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/profile/js-min"));
  done();
});

// minify basejs
task("basejs", (done) => {
  src("TourDay/static/js/base.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/js-min"));
  done();
});

// minify croppiejs
task("croppiejs", (done) => {
  src("TourDay/static/js/croppie.js")
    .pipe(uglify())
    .pipe(dest("TourDay/static/js-min"));
  done();
});

// minify mainjs
task("mainjs", (done) => {
  src("TourDay/static/blog/js/main.js")
    .pipe(uglify())
    .pipe(rename({ suffix: ".min" }))
    .pipe(dest("TourDay/static/blog/js"));
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
  watch("TourDay/static/_auth/js/forgetpassword.js", series("forgetjs"));
  watch("TourDay/static/_auth/js/login.js", series("loginjs"));
  watch("TourDay/static/_auth/js/resetpassword.js", series("resetjs"));
  watch("TourDay/static/_auth/js/signup.js", series("signupjs"));
  watch("TourDay/static/event/js/dashboard.js", series("dashboardjs"));
  watch("TourDay/static/event/js/event.js", series("eventjs"));
  watch("TourDay/static/profile/js/map.js", series("mapjs"));
  watch("TourDay/static/profile/js/portfolio.js", series("portfoliojs"));
  watch("TourDay/static/profile/js/profile.js", series("profilejs"));
  watch("TourDay/static/js/base.js", series("basejs"));
  watch("TourDay/static/blog/js/main.js", series("mainjs"));
});

task(
  "default",
  series(
    "base",
    "croppie",
    "layout",
    "event",
    "dashboard",
    "map",
    "portfolio",
    "profile",
    "style",
    "search",
    "forgetjs",
    "loginjs",
    "resetjs",
    "signupjs",
    "dashboardjs",
    "eventjs",
    "mapjs",
    "portfoliojs",
    "profilejs",
    "basejs",
    "croppiejs",
    "mainjs"
  )
);
