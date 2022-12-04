function add_and_update_cart(item_id) {

    let product_id = item_id;
    //const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    //var csrftoken = getCsrf();
    const csrftoken = csrf;
    fetch('/cart/add_js', {
      headers: {
          'Content-Type': 'application/json',
          //'X-CSRFToken': '{{ csrf_token }}',
          'X-CSRFToken': csrftoken,

      },
      method: 'POST',
      body: JSON.stringify({
        //csrfmiddlewaretoken: '{{ csrf_token }}',  
        "product_id": product_id,
        //action : 'post'
      })
  }).then(function (response) {
      if (response.ok) {
          response.json().then(function (response) {
              //console.log(response.cart_len);
              document.getElementById('cart_len').innerHTML = response.cart_len;
              document.getElementById('cart_sum').innerHTML = response.cart_sum;
              alert("Thank you, the item has been added to the cart");
          });
      } else {
          throw Error('Something went wrong');
      }
  }).catch(function (error) {
      console.log(error);
  });
 }

