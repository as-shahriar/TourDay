
document.querySelectorAll(".open-modal").forEach(e=>{
    e.addEventListener("click",()=>{
        id = e.getAttribute("data-id")
        get_product_info(id)
    })
})


function get_product_info(id){
    fetch(`/api/shop/product/details/${id}`).
    then(res=>res.json()).
    then(data=>{
        const {description, image,name,price,product_type,digital} = data
        changeModal(id,name,description,price,image,product_type,digital)
        document.getElementById("modal-triger").click();
    })
}



changeModal = (id,title,description,price,img,product_type,digital)=>{

    document.getElementById("product_details").setAttribute('data-product', id);
    
    document.getElementById("modal-img").src = img
    document.getElementById("modal-title").textContent = title
    document.getElementById("modal-price").textContent = `৳${price}`
    document.getElementById("modal-product_type").textContent = `Category : ${product_type}`
    if(digital === false) {
        document.getElementById("modal-status").textContent = 'In Stock'
        document.getElementById("modal-status").style.color = "green";
        document.getElementById("product_details").disabled = false;
        document.getElementById("product_details").style.cursor = "pointer";
    }
    else {
        document.getElementById("modal-status").textContent = 'Out Stock'
        document.getElementById("modal-status").style.color = "red";
        document.getElementById("product_details").disabled = true;
        document.getElementById("product_details").style.cursor = "default";
    }
    document.getElementById("modal-description").textContent = description
    
}


url = window.location.href;
re = /#[0-9]+/
value_in_url = re.exec(url)
if (value_in_url){
    id = value_in_url[0].replace(/#/,"")
    get_product_info(id)
}
