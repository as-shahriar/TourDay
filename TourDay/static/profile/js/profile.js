btn_name = $("#btn-name");
btn_email = $("#btn-email");
btn_fb = $("#btn-fb");
btn_password = $("#btn-password");
btn_bio = $("#btn-bio");
btn_city = $("#btn-city");

inputs = ["name", "email", "fb", "password", "bio", "city"];
inputs.forEach((element) => {
  document
    .querySelector(`#input-${element}`)
    .addEventListener("keyup", function (event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        show_hide(element);
      }
    });
});

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
      } else if (response.status == 201) {
        if (param != "password") {
          $(`#${param}`).text(data);
        }
        if (param === "name") {
          $("#name_pic").text(data);
        }
      }
    },
    error: (res) => {
      $("#error-msg").text("Network error.");
      $(".error").show();
      hide_error();
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

// Upload Image
document.getElementById("selectedFile").onchange = () => {
  let picture = document.getElementById("selectedFile");
  var name = picture.files[0].name;
  var form_data = new FormData();
  var ext = name.split(".").pop().toLowerCase();
  var oFReader = new FileReader();
  oFReader.readAsDataURL(picture.files[0]);
  var f = picture.files[0];
  var fsize = f.size || f.fileSize;
  if (jQuery.inArray(ext, ["gif", "png", "jpg", "jpeg"]) == -1) {
    alert("Invalid Image File");
  } else if (fsize > 2000000) {
    alert("Upload small size image");
  } else {
    form_data.append("picture", picture.files[0]);
    form_data.append("csrfmiddlewaretoken", getCookie("csrftoken"));
    $.ajax({
      url: "/profile/picture",
      method: "POST",
      data: form_data,
      contentType: false,
      cache: false,
      enctype: "multipart/form-data",
      processData: false,
      beforeSend: function () {
        // $(".loader").show();
      },
      success: function (data) {
        // $(".loader").hide();
        if ((data.status = "201")) {
          document.getElementById("pro_pic").src = data.new_img;
        }
      },
    });
  }
};
