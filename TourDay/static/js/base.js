$(window).on("load", function () {
  setInterval(() => {
    $(".loader").hide();
    $("body").css({ overflow: "visible" });
  }, 1000);
});

function validateEmail(email) {
  var re = /\S+@\S+\.\S+/;
  return re.test(email);
}

function validateUsername(username) {
  var re = /^[a-zA-Z]{3}[a-z0-9_]*$/;
  return re.test(username);
}

let timeout = undefined;

isCliked = false;
document.querySelector(".menu-icon").addEventListener("click", () => {
  document.querySelector(".menu-icon").classList.toggle("active");
  document.querySelector("#items").classList.toggle("open");
  if (!isCliked) {
    setTimeout(() => {
      document.querySelector(".menu-mobile").classList.toggle("showNav");
    }, 130);
    document.querySelector(".menu-icon").classList.toggle("addColor");
    isCliked = true;
  } else {
    document.querySelector(".menu-mobile").classList.toggle("showNav");
    document.querySelector(".menu-icon").classList.toggle("addColor");
    isCliked = false;
  }
});

$("#close-error").click(function () {
  //hide error on click close button
  $(".error").hide();
  if (timeout != undefined) {
    clearTimeout(timeout);
  }
});

//return csrf token
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function hide_error() {
  timeout = setTimeout(() => $(".error").hide(), 5000);
}


function loader_progress(){
  loader_length = 0;
  document.getElementById("upper_loader").style.display = "block";
  return setInterval(()=>{
    document.getElementById("upper_loader").style.width = `${loader_length}%`;
    if(loader_length<80)
      loader_length += 4;
    else if (loader_length>=80 && loader_length<101)
    loader_length += 0.07;
    
  },1);
}

function clear_loader_progress(interval){
  
  setTimeout(()=>{
    clearInterval(interval);
  document.getElementById("upper_loader").style.display = "none";},800);
}