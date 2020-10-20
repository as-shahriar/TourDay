$("#login").click(function (e) {
  e.preventDefault();
  var username = $("#username");
  var password = $("#password");

  if (username.val() == "") {
    username.addClass("input-error");
    return;
  } else {
    username.removeClass("input-error");
  }
  if (password.val() == "") {
    password.addClass("input-error");
    return;
  } else {
    password.removeClass("input-error");
  }
  interval = loader_progress();
  
  $.ajax({
    url: "/login/",
    type: "POST",
    data: {
      username: username.val(),
      password: password.val(),
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },

    success: function (result) {
      if (result.status == 200) {
        redirect();
      } else {
        $(".error").show();
        hide_error();
      }
    },
    error: function (result) {
      console.log("Network Error");
    },
    complete: function(result){
      clear_loader_progress(interval);
    }
  });
});

function redirect() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  if (urlParams.has("next")) {
    const next = urlParams.get("next");
    location.href = next;
  } else {
    location.href = "/";
  }
}
