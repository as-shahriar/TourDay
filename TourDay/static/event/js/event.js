function isFileImage(file) {
  const acceptedImageTypes = [
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
  ];

  return file && acceptedImageTypes.includes(file["type"]);
}

select_picture = document.getElementById("image");
pic_btn = document.getElementById("pic-btn");
preview_div = document.getElementById("img-preview");
preview_close = document.getElementById("preview-close");
pic_preview = document.getElementById("pic_preview");

if (select_picture != null) {
  select_picture.addEventListener("change", () => {
    const file = select_picture.files[0];
    if (!isFileImage(file)) {
      select_picture.value = "";
      return;
    }
    previewFile(file);
    pic_btn.style.display = "none";

    preview_div.style.display = "block";
  });

  preview_close.addEventListener("click", () => {
    pic_btn.style.display = "block";
    preview_div.style.display = "none";
    select_picture.value = "";
  });
}

function previewFile(file) {
  const reader = new FileReader();

  reader.addEventListener(
    "load",
    function () {
      // convert image file to base64 string
      pic_preview.src = reader.result;
    },
    false
  );

  if (file) {
    reader.readAsDataURL(file);
  }
}

document.getElementById("edit-event").addEventListener("click", () => {
  id = document.getElementById("id").value;
  title = document.getElementById("title").value;
  location_ = document.getElementById("location").value;
  date = document.getElementById("date").value;
  details = document.getElementById("details").value;
  if (title == "" || location_ == "" || date == "" || details == "") {
    $("#error-msg").text("Fill up all fileds.");
    $(".error").show();
    hide_error();
    return;
  }
  form = new FormData();
  form.append("title", title);
  form.append("location", location_);
  form.append("date", date);
  form.append("details", details);
  form.append("pay1", document.getElementById("pay1").value);
  form.append("pay2", document.getElementById("pay2").value);
  form.append("pay1_method", document.getElementById("pay1_method").value);
  form.append("pay2_method", document.getElementById("pay2_method").value);
  form.append("image", select_picture.files[0]);
  console.log(select_picture.files[0]);

  fetch(`/event/edit_events/${id}`, {
    method: "POST",
    body: form,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status == 200) {
        location.href = `/event/${data.id}`;
      }
    });
});

function copy_url() {
  var dummy = document.createElement("input"),
    text = window.location.href;
  document.body.appendChild(dummy);
  dummy.value = text;
  dummy.select();
  document.execCommand("copy");
  document.body.removeChild(dummy);
}

document.getElementById("copy-url").addEventListener("click", copy_url);
