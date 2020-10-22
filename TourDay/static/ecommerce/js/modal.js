
document.querySelectorAll(".open-modal").forEach(e=>{
    e.addEventListener("click",()=>{
        id = e.getAttribute("data-id")
        fetch(`/api/ecommerce/product/details/${id}`).
        then(res=>res.json()).
        then(data=>{
            const {description, image,name,price,product_type,digital} = data
            changeModal(id,name,description,price,image,product_type,digital)
            document.getElementById("modal-triger").click();
        })
    })
})

changeModal = (id,title,description,price,img,product_type,digital)=>{
    document.getElementById("modal-img").src = img
    document.getElementById("modal-title").textContent = title
    document.getElementById("modal-price").textContent = `৳${price}`
    document.getElementById("modal-product_type").textContent = `Category : ${product_type}`
    if(digital === false) {
        document.getElementById("modal-status").textContent = 'In Stock'
        document.getElementById("modal-status").style.color = "green";
    }
    else {
        document.getElementById("modal-status").textContent = 'Out Stock'
        document.getElementById("modal-status").style.color = "red";
    }
    document.getElementById("modal-description").textContent = description
    
}
