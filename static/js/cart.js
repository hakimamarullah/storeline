let updateBtns = document.getElementsByClassName("update-cart")

for(let i=0; i<updateBtns.length; i++){
	updateBtns[i].addEventListener("click", function(){
		let productId = this.dataset.product
		let action = this.dataset.action
		let output = {'productId': productId, 'action':action}
		console.log(output)

		if(user == "AnonymousUser"){
			console.log("You're not logged in...")
		}
		else{
			updateUserOrder(productId, action)
		}
	})

}

function updateUserOrder(productId, action){
	console.log("Sending data...")

	url = '/update-item/'

	fetch(url,{
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({"productId":productId, 'action':action})
	})

	.then((response)=>{
		return response.json()
	})

	.then((data)=>{
		console.log(data)
		location.reload()
	})
}