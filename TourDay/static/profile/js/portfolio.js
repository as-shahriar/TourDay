select_picture = document.getElementById("picture");
pic_btn = document.getElementById("pic-btn");
preview_div = document.getElementById("preview");
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

function isFileImage(file) {
  const acceptedImageTypes = [
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
  ];

  return file && acceptedImageTypes.includes(file["type"]);
}

function add_post(root, id, post, date, img_src, like, like_btn, location) {
  like_btn_icon = "/static/icon/like.png";
  dislike_btn_icon = "/static/icon/like2.png";
  post_section = document.getElementById(root);
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
  p.textContent = post;
  div_img = document.createElement("div");
  div_img.setAttribute("class", "post-img");
  img2 = document.createElement("img");
  img2.setAttribute("data-toggle", "modal");
  img2.setAttribute("data-target", ".modal-image");
  img2.setAttribute("id", `post-image-${id}`);
  img2.setAttribute("src", img_src);
  img2.addEventListener("click", () => {
    //modal to copy from content
    document.getElementById("post-image-modal").src = img_src;
  });
  div_lower = document.createElement("div");
  div_lower.setAttribute("class", "lower");
  div = document.createElement("div");
  img3 = document.createElement("img");

  if (like_btn) {
    img3.setAttribute("src", like_btn_icon);
    img3.setAttribute("data-is-liked", "1"); //1 for liked
  } else {
    img3.setAttribute("src", dislike_btn_icon);
    img3.setAttribute("data-is-liked", "0"); //0 for unliked
  }
  img3.setAttribute("id", `like-btn-${id}`);
  img3.setAttribute("class", "like");
  img3.addEventListener("click", (e) => {
    is_liked = e.target.getAttribute("data-is-liked");

    element = document.getElementById(`like-btn-${id}`);
    like_count_text = document.getElementById(`like-count-${id}`);
    if (is_liked == "1") {
      element.setAttribute("src", dislike_btn_icon);
      element.setAttribute("data-is-liked", "0");
      like_count_text.textContent = parseInt(like_count_text.textContent) - 1;
    } else {
      element.setAttribute("src", like_btn_icon);
      element.setAttribute("data-is-liked", "1");
      like_count_text.textContent = parseInt(like_count_text.textContent) + 1;
    }
    like_event(id);
  });
  span1 = document.createElement("span");
  span1.setAttribute("id", `like-count-${id}`);
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
  if (img_src != null) div_body.appendChild(div_img);
  div_body.appendChild(div_lower);
  div_user_info.appendChild(img);
  div_user_info.appendChild(span);
  div_head.appendChild(div_user_info);
  div_head.appendChild(div_date);
  div_post.appendChild(div_head);
  div_post.appendChild(div_body);

  post_section.appendChild(div_post);
}

let next;

function get_post(url) {
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      next = data.next;

      data.results.forEach((post) => {
        add_post(
          "post-section",
          post.id,
          post.post,
          post.date,
          post.image,
          post.likes.length,
          post.likes.includes(
            parseInt(document.getElementById("user-id").value)
          ),
          post.location
        );
      });
    });
}

if (next != null) {
  $(window).scroll(function () {
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
      get_post(next);
    }
  });
}

$(document).ready(() => {
  username = document.getElementById("my-username").value;
  get_post(`/get_post/${username}?format=json`);
});

function like_event(id) {
  form = new FormData();
  form.append("id", id);

  fetch("/like/", {
    method: "POST",
    body: form,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status != 200) {
        console.log("Like error.");
      }
    });
}

// set Current Date
function set_current_date() {
  Date.prototype.toDateInputValue = function () {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
  };
  document.getElementById("date").value = new Date().toDateInputValue();
}

document.getElementById("post-btn").addEventListener("click", () => {
  post = document.getElementById("add-post-text");
  date = document.getElementById("date");
  location_ = document.getElementById("city");
  file = select_picture.files[0];

  if (post.value == "" || location_.value == "null" || file == null) return;
  form = new FormData();
  form.append("post", post.value);
  form.append("date", date.value);
  form.append("location", location_.value);
  form.append("image", file);

  fetch("/add_post/", {
    method: "POST",
    body: form,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status == 201) {
        add_post(
          "new-post",
          data.id,
          post.value.trim(),
          date.value,
          data.image,
          0,
          false,
          data.location
        );
        preview_close.click();
        post.value = "";
        set_current_date();
      } else {
        console.log("uploading error");
      }
    });
});

set_current_date();
