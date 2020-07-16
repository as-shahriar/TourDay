btn_name = $("#btn-name");
btn_email = $("#btn-email");
btn_fb = $("#btn-fb");
btn_password = $("#btn-password");
btn_bio = $("#btn-bio");
btn_city = $("#btn-city");

function show_hide(component) {
  value = document.querySelector(`#btn-${component}`);
  if (value.innerHTML === "Edit") {
    value.innerHTML = "Save";
    $(`#input-${component}`).show();
    $(`#${component}`).hide();
  } else {
    if (!validate_info(component, $(`#input-${component}`).val())) return;
    add_info(component, $(`#input-${component}`).val());
    value.innerHTML = "Edit";
    $(`#input-${component}`).hide();
    $(`#${component}`).show();
  }
}

btn_name.on("click", () => {
  show_hide("name");
});
btn_email.on("click", () => {
  show_hide("email");
});
btn_fb.on("click", () => {
  show_hide("fb");
});
btn_password.on("click", () => {
  show_hide("password");
});
btn_bio.on("click", () => {
  show_hide("bio");
});
btn_city.on("click", () => {
  show_hide("city");
});

function add_info(param, data) {
  console.log(data);
  $.ajax({
    type: "POST",
    url: `/profile/${param}`,
    data: {
      data: data,
      csrfmiddlewaretoken: getCookie("csrftoken"),
    },
    success: function (response) {
      if (response.status == 400) {
        $("#error-msg").text("Email address already exists.");
        $(".error").show();
        hide_error();
        btn_email.click();
      }
    },
  });
}

function validate_info(param, data) {
  if (param === "password" && data.length < 8) {
    $("#error-msg").text("Password must contain at least 8 Characters.");
    $(".error").show();
    hide_error();
    return false;
  }
  if (param === "email" && !validateEmail(data)) {
    $("#error-msg").text("Invalid Email Address.");
    $(".error").show();
    hide_error();
    return false;
  }

  return true;
}
