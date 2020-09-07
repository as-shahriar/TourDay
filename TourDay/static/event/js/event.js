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
