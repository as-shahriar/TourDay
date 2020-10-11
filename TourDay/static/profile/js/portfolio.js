select_picture = document.getElementById("picture");
pic_btn = document.getElementById("pic-btn");
preview_div = document.getElementById("preview");
preview_close = document.getElementById("preview-close");
pic_preview = document.getElementById("pic_preview");

post_loader = document.getElementById("post-loder");
see_more = document.querySelector("#see-more");
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

  document.getElementById("post-btn").addEventListener("click", () => {
    post = document.getElementById("add-post-text");
    date = document.getElementById("date");
    location_ = document.getElementById("city");
    file = select_picture.files[0];

    if (post.value == "" || location_.value == "null" || file == null) {
      $("#error-msg").text("All fileds are required.");
      $(".error").show();
      hide_error();
      return;
    }

    form = new FormData();
    form.append("post", post.value);
    form.append("date", date.value);
    form.append("location", location_.value);
    form.append("image", file);

    interval = loader_progress();
    fetch("/add_post/", {
      method: "POST",
      body: form,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status == 201) {
          add_post(
            false,
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
          get_map_data();
        } else {
          console.log("uploading error");
        }
        clear_loader_progress(interval);
      });
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

// direction true to append false to prepend
function add_post(
  direction,
  id,
  post,
  date,
  img_src,
  like,
  like_btn,
  location
) {
  like_btn_icon = "/static/icon/like.png";
  dislike_btn_icon = "/static/icon/like2.png";
  post_section = document.getElementById("post-section");
  div_post = document.createElement("div");
  div_post.setAttribute("class", "post");
  div_post.setAttribute("id", `post-div-${id}`);
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
  div_date.setAttribute("class", "date-div");
  span_date = document.createElement("span");
  span_date.textContent = date;

  div_date.appendChild(span_date);
  if (select_picture != null) {
    i_delete = document.createElement("i");
    i_delete.setAttribute("class", "material-icons");
    i_delete.textContent = "delete";

    i_delete.addEventListener("click", () => {
      delete_post(id);
    });
    div_date.appendChild(i_delete);
  }
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
  if(post_section!=null){
  if (direction) post_section.appendChild(div_post);
  else post_section.prepend(div_post);}
}

let next;

function get_post(url) {
  fetch(url)
    .then((res) => res.json())
    .then((data) => {
      next = data.next;
      if (data.next) see_more.style.display = "block";
      else {
        see_more.style.display = "none";
        document.querySelector("#hr-hide-with-see-more").style.display = "none";
    }
      if (post_loader !=null)
      post_loader.style.display = "none";
      
      data.results.forEach((post) => {
        add_post(
          true,
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

see_more.addEventListener("click",()=>{
  if(next){
    if (post_loader !=null)
  post_loader.style.display = "flex";
  get_post(next);
}
});

  $(window).scroll(function () {
    if($(window).width()>783){
    if ($(window).scrollTop() + $(window).height() >= $(document).height()-1) {
      if(next){
      get_post(next);
      if (post_loader !=null)
      post_loader.style.display = "flex";}
    }}
  });


$(document).ready(() => {
  username = document.getElementById("my-username").value;
  if (select_picture != null) set_current_date();
  get_map_data();
  get_post(`/get_post/${username}?format=json`);
});

function like_event(id) {
  form = new FormData();
  form.append("id", id);
  interval = loader_progress();
  fetch("/like/", {
    method: "POST",
    body: form,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status != 200) {
        console.log("Like error.");
      }
      
      clear_loader_progress(interval);
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

function delete_post(id) {
  form = new FormData();
  form.append("id", id);
  interval = loader_progress();
  fetch("/delete_post/", {
    method: "POST",
    body: form,
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status == 200) {
        elem = document.getElementById(`post-div-${id}`);
        elem.parentNode.removeChild(elem);
        clear_loader_progress(interval);
      }
    });
}

function get_map_data() {
  user = document.getElementById("my-username").value;
  fetch(`/visited/${user}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.status == 200) {
        data.visited.forEach((e) => {
          document.getElementById(`path${e}`).style.fill = "#940808";
        });
      }
    });
}
