
document.querySelectorAll(".open-modal").forEach(e=>{
    e.addEventListener("click",()=>{
        id = e.getAttribute("data-id")
        fetch(`/api/ecommerce/product/details/${id}`).
        then(res=>res.json()).
        then(data=>{
            const {discription, image,name,price} = data
            changeModal(id,name,discription,price,image)
            document.getElementById("modal-triger").click();
        })
    })
})

changeModal = (id,title,description,price,img)=>{
    document.getElementById("modal-img").src = img
    document.getElementById("modal-title").textContent = title
    document.getElementById("modal-description").textContent = description
    document.getElementById("modal-price").textContent = `৳${price}`
}