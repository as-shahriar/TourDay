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
