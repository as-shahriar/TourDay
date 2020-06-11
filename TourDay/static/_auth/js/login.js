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

  $.ajax({
    url: "/ajaxlogin",
    type: "POST",
    data: {
      username: username.val(),
      password: password.val(),
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },

    success: function (result) {
      console.log(result.status);
      if (result.status == 200) {
        location.href = "/";
      } else {
        $(".error").show();
      }
    },
    error: function (result) {
      console.log(result);
    },
  });
});
