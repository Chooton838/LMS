var updateBtns = document.getElementsByClassName('update-cart')

for (var i =0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        var pk = this.dataset.pk

        updateUserOrder(productId, action, pk)

    })

}

function updateUserOrder(productId, action, pk){

    var url = '/staff/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action, 'pk': pk})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}