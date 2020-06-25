$("#save").click(function (e) {
  e.preventDefault();
  var code = $("#code");
  var password1 = $("#password1");
  var password2 = $("#password2");
  var username = $("#slug");

  if (code.val() == "" || code.val().length != 8) {
    code.addClass("input-error");
    return;
  } else {
    code.removeClass("input-error");
  }
  if (password1.val() == "") {
    password1.addClass("input-error");
    return;
  } else {
    password1.removeClass("input-error");
  }
  if (password2.val() == "") {
    password2.addClass("input-error");
    return;
  } else {
    password2.removeClass("input-error");
  }

  if (password1.val().length < 8) {
    $("#error-msg").text("Password must contain at least 8 Characters.");
    $(".error").show();
    hide_error();
    password1.addClass("input-error");
    return;
  } else {
    password1.removeClass("input-error");
  }
  if (password1.val() != password2.val()) {
    $("#error-msg").text("Password didn't match.");
    $(".error").show();
    hide_error();
    password1.addClass("input-error");
    password2.addClass("input-error");
    return;
  } else {
    password1.removeClass("input-error");
    password2.removeClass("input-error");
  }

  $.ajax({
    url: "/reset-password/" + username.val(),
    type: "POST",
    data: {
      code: code.val(),
      username: username.val(),
      password1: password1.val(),
      password2: password2.val(),
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },

    success: function (result) {
      if (result.status == 200) {
        location.href = "/";
      } else {
        $("#error-msg").text("Invalid Credentials.");
        $(".error").show();
        hide_error();
      }
    },
    error: function (result) {
      console.log("Network Error");
    },
  });
});
