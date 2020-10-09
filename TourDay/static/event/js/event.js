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

edit_btn = document.getElementById("edit-event");
if (edit_btn != null) {
  edit_btn.addEventListener("click", () => {
    id = document.getElementById("id").value;
    title = document.getElementById("title").value;
    location_ = document.getElementById("location").value;
    date = document.getElementById("date").value;
    details = document.getElementById("details").value;
    cost = document.getElementById("cost").value;
    capacity = document.getElementById("capacity").value;
    if (
      title == "" ||
      location_ == "" ||
      date == "" ||
      details == "" ||
      cost == "" ||
      capacity == ""
    ) {
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
    form.append("cost", cost);
    form.append("capacity", capacity);
    form.append("pay1", document.getElementById("pay1").value);
    form.append("pay2", document.getElementById("pay2").value);
    form.append("pay1_method", document.getElementById("pay1_method").value);
    form.append("pay2_method", document.getElementById("pay2_method").value);
    form.append("image", select_picture.files[0]);
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
}
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

document.querySelectorAll(".accept-btn").forEach((e) => {
  e.addEventListener("click", () => {
    user_id = e.dataset.id;
    id = document.getElementById("id").value;
    form = new FormData();
    form.append("is_accepted", "1");
    form.append("user_id", user_id);
    fetch(`/event/action/${id}`, {
      method: "POST",
      body: form,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status == 200) {
          add_going(data.username, data.img, data.name, data.email);
          hide_pending(user_id);
        }
      });
  });
});

document.querySelectorAll(".cancel-btn").forEach((e) => {
  e.addEventListener("click", () => {
    user_id = e.dataset.id;
    id = document.getElementById("id").value;
    form = new FormData();
    form.append("is_accepted", "0");
    form.append("user_id", user_id);
    fetch(`/event/action/${id}`, {
      method: "POST",
      body: form,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status == 200) {
          hide_pending(user_id);
        }
      });
  });
});

function add_going(username, img, name, email) {
  a = document.createElement("a");
  a.setAttribute("href", `/u/${username}`);

  div = document.createElement("div");
  div.setAttribute("class", "travelers");
  img_ = document.createElement("img");
  img_.setAttribute("src", img);
  h5_1 = document.createElement("h5");
  h5_1.textContent = name;
  h5_2 = document.createElement("h5");
  h5_2.textContent = email;

  div.appendChild(img_);
  div.appendChild(h5_1);
  div.appendChild(h5_2);
  a.appendChild(div);
  document.getElementById("going-list").appendChild(a);
  counter = document.getElementById("going-count");
  counter2 = document.getElementById("going-count-2");
  counter.textContent = parseInt(counter.textContent) + 1;
  counter2.textContent = counter.textContent;
}

function hide_pending(id) {
  document.getElementById(`pending-${id}`).style.display = "none";
  counter = document.getElementById("pending-counter");
  counter.textContent = parseInt(counter.textContent) - 1;
}

join_send_btn = document.getElementById("join-send-btn");
if (join_send_btn != null) {
  join_send_btn.addEventListener("click", () => {
    id = document.getElementById("id").value;
    tr = document.getElementById("tr-id").value;
    method = document.getElementById("pay_method").value;
    if (tr == "") {
      $("#error-msg").text("Transaction ID is required");
      $(".error").show();
      hide_error();
      return;
    }

    form = new FormData();
    form.append("method", method);
    form.append("tr", tr);

    fetch(`/event/pay/${id}`, { method: "POST", body: form })
      .then((res) => res.json())
      .then((data) => {
        if (data.status == 200) {
          h3 = document.createElement("h3");
          span = document.createElement("span");
          span.setAttribute("class", "badge badge-info px-5 py-2");
          span.textContent = "Payment Pending";
          h3.appendChild(span);
          document.getElementById("payment-div").appendChild(h3);
          document.getElementById("join-modal-btn").style.display = "none";
          counter = document.getElementById("pending-counter");
          counter.textContent = parseInt(counter.textContent) + 1;
          document.getElementById("close-modal").click();
        }
      });
  });
}

delete_btn = document.getElementById("delete-btn");

if (delete_btn != null) {
  delete_btn.addEventListener("click", () => {
    var r = confirm("Delete this event?");
    if (r) {
      id = document.getElementById("id").value;
      fetch(`/event/delete/${id}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.status == 200) {
            location.href = "/event/dashboard";
          }
        });
    }
  });
}
