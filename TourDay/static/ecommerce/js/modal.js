
document.querySelectorAll(".open-modal").forEach(e=>{
    e.addEventListener("click",()=>{
        id = e.getAttribute("data-id")
        get_product_info(id)
    })
})

changeModal = (id,title,description,price,img)=>{
    document.getElementById("modal-img").src = img
    document.getElementById("modal-title").textContent = title
    document.getElementById("modal-description").textContent = description
    document.getElementById("modal-price").textContent = `৳${price}`
}

get_product_info = (id)=>{
    fetch(`/api/ecommerce/product/details/${id}`).
    then(res=>res.json()).
    then(data=>{
        const {discription, image,name,price} = data
        changeModal(id,name,discription,price,image)
        document.getElementById("modal-triger").click();
    })
}

url = window.location.href;
re = /#[0-9]+/
value_in_url = re.exec(url)
if (value_in_url){
    id = value_in_url[0].replace(/#/,"")
    get_product_info(id)
}
