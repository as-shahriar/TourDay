$("#getcode").click(function (e) {
  e.preventDefault();
  var username = $("#username");

  if (username.val() == "") {
    username.addClass("input-error");
    return;
  } else {
    username.removeClass("input-error");
  }

  $.ajax({
    url: "/forget-password/",
    type: "POST",
    data: {
      username_email: username.val(),
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },

    success: function (result) {
      if (result.status == 200) {
        location.href = "/reset-password/" + result.slug;
      } else {
        $("#error-msg").text("Wrong username or email address.");
        $(".error").show();
        hide_error();
      }
    },
    error: function (result) {
      console.log("Network Error");
    },
  });
});
