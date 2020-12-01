var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}

function addCookieItem(productId, action){
	

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			
			delete cart[productId];
		}
	}
	
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}


// Preloader 
$(window).on("load", function () {
	// makes sure the whole site is loaded
	$("#status").fadeOut(); // will first fade out the loading animation
	$("#preloader").delay(350).fadeOut("slow"); // will fade out the white DIV that covers the website.
	$("body").delay(350).css({ overflow: "visible" });
  });