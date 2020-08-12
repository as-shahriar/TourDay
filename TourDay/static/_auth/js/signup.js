$("#username").change(() => {
  var username = $("#username");

  if (username.val() != "") {
    if (!validateUsername(username.val())) {
      $("#error-msg").text("Invalid Username.");
      $(".error").show();
      hide_error();
      username.addClass("input-error");
      return;
    }

    $.ajax({
      url: "/checkusername",
      type: "POST",
      data: {
        username: username.val(),
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },

      success: function (result) {
        if (result.status == 404) {
          username.removeClass("input-error");
        } else {
          $("#error-msg").text("Username already exists.");
          $(".error").show();
          hide_error();
          username.addClass("input-error");
        }
      },
      error: function (result) {
        console.log("Network Error");
      },
    });
  }
});

$("#email").change(() => {
  var email = $("#email");

  if (email.val() != "") {
    if (!validateEmail(email.val())) {
      $("#error-msg").text("Invalid Email Address.");
      $(".error").show();
      hide_error();
      email.addClass("input-error");
      return;
    }

    $.ajax({
      url: "/checkemail",
      type: "POST",
      data: {
        email: email.val(),
        csrfmiddlewaretoken: getCookie("csrftoken"),
      },

      success: function (result) {
        if (result.status == 404) {
          email.removeClass("input-error");
        } else {
          $("#error-msg").text("Email address already exists.");
          $(".error").show();
          hide_error();
          email.addClass("input-error");
        }
      },
      error: function (result) {
        console.log("Network Error");
      },
    });
  }
});

$("#signup").click(function (e) {
  e.preventDefault();
  var username = $("#username");
  var password = $("#password");
  var email = $("#email");

  if (username.val() == "" || !validateUsername(username.val())) {
    username.addClass("input-error");
    $("#error-msg").text("Invalid Username.");
    $(".error").show();
    hide_error();
    return;
  } else {
    username.removeClass("input-error");
  }

  if (email.val() == "" || !validateEmail(email.val())) {
    $("#error-msg").text("Invalid Email Address.");
    $(".error").show();
    hide_error();
    email.addClass("input-error");
    return;
  } else {
    email.removeClass("input-error");
  }
  if (password.val() == "" || password.val().length < 8) {
    $("#error-msg").text("Password must contain at least 8 Characters.");
    $(".error").show();
    hide_error();
    password.addClass("input-error");
    return;
  } else {
    password.removeClass("input-error");
  }

  $.ajax({
    url: "/signup/",
    type: "POST",
    data: {
      username: username.val(),
      email: email.val(),
      password: password.val(),
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },

    success: function (result) {
      if (result.status == 200) {
        location.href = "/profile";
      } else {
        $("#error-msg").text("Username or Email already Exists.");
        $(".error").show();
        hide_error();
      }
    },
    error: function (result) {
      console.log("Network Error");
    },
  });
});
