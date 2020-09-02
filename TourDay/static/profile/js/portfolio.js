select_picture = document.getElementById("picture");
pic_btn = document.getElementById("pic-btn");
preview_div = document.getElementById("preview");
preview_close = document.getElementById("preview-close");
pic_preview = document.getElementById("pic_preview");

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

function isFileImage(file) {
  const acceptedImageTypes = [
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
  ];

  return file && acceptedImageTypes.includes(file["type"]);
}

function add_post(date, img_src, like, location) {
  post_section = document.getElementById("post-section");
  div_post = document.createElement("div");
  div_post.setAttribute("class", "post");
  div_head = document.createElement("div");
  div_head.setAttribute("class", "post-head");
  div_user_info = document.createElement("div");
  div_user_info.setAttribute("class", "user-info");

  img = document.createElement("img");
  img.setAttribute("class", "user-img");
  img.setAttribute("src", document.getElementById("pro_pic").src);

  span = document.createElement("span");
  span.textContent = document.getElementById("name").textContent;

  div_date = document.createElement("div");
  div_date.textContent = date;
  div_body = document.createElement("div");
  div_body.setAttribute("class", "post-body");
  p = document.createElement("p");
  p.setAttribute("class", "post-text");
  p.textContent = "loasdasd lkjf hsdfsa ihsadfhlkjsdahkjsdflkj fhkjs";
  div_img = document.createElement("div");
  div_img.setAttribute("class", "post-img");
  img2 = document.createElement("img");
  img2.setAttribute("data-toggle", "modal");
  img2.setAttribute("data-target", ".modal-image");
  img2.setAttribute("src", img_src);
  div_lower = document.createElement("div");
  div_lower.setAttribute("class", "lower");
  div = document.createElement("div");
  img3 = document.createElement("img");
  img3.setAttribute("src", document.getElementById("like-icon").src);
  img3.setAttribute("class", "like");
  span1 = document.createElement("span");
  span1.textContent = like;
  div_location = document.createElement("div");
  div_location.setAttribute("class", "location-div");

  i = document.createElement("i");
  i.setAttribute("class", "material-icons");
  i.textContent = "location_on";
  span2 = document.createElement("span");
  span2.textContent = location;

  div_location.appendChild(i);
  div_location.appendChild(span2);
  div.appendChild(img3);
  div.appendChild(span1);
  div_lower.appendChild(div);
  div_lower.appendChild(div_location);
  div_img.appendChild(img2);
  div_body.appendChild(p);
  div_body.appendChild(div_img);
  div_body.appendChild(div_lower);
  div_user_info.appendChild(img);
  div_user_info.appendChild(span);
  div_head.appendChild(div_user_info);
  div_head.appendChild(div_date);
  div_post.appendChild(div_head);
  div_post.appendChild(div_body);

  post_section.appendChild(div_post);
}

add_post("August 20, 2001", "https://bit.ly/2E0HhlL", 2, "Dhaka");
