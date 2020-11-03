$(window).scroll(function () {
    if($(window).width()>783){
        if ($(window).scrollTop() + $(window).height() >= $(document).height()-1) {
            console.log(next)
        if(next){
            
            get_data(next);
            }
        }
    }
  });

var next;

function get_data (url){
    fetch(url).
    then(res=>res.json()).
    then(data=>{
        next = data.next;
        if(!next){
            document.getElementById("see-more-div").style.display = "none"
        }
        data.results.forEach(element => {
            add_event(element.id,element.title,element.location,element.date)
        });
    });
}

add_event = (id,title,_location,date) =>{
    a = document.createElement("a")
    a.setAttribute("href",`/event/${id}`)
    li = document.createElement("li")
    li.setAttribute("class","users mb-3")
    div = document.createElement("div")
    div.setAttribute("class","user-details")
    h5_1 = document.createElement("h5")
    h5_1.textContent = title
    h5_2 = document.createElement("h5")
    h5_2.setAttribute("class","small-font")
    h5_2.textContent = _location
    h5_3 = document.createElement("h5")
    h5_3.setAttribute("class","small-font")
    h5_3.textContent = date

    div.appendChild(h5_1)
    div.appendChild(h5_2)
    div.appendChild(h5_3)
    li.appendChild(div)
    a.appendChild(li)
    document.getElementById("event-root").appendChild(a)
}

get_data("/event/all-events/");

document.getElementById("see-more-div").addEventListener("click",()=>get_data(next))

