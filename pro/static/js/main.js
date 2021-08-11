function print(p) {
  console.log(p);
}
$(".update-cart").on("click", function () {
  action = this.dataset.action;
  productId = this.dataset.product;
  print(user);
  if (user == "AnonymousUser") {
    print("not authenticated user");
    $(".toast").addClass('bg-info')
    $(".toast .toast-body").text('please login first to get add to cart')
    $(".toast").toast("show")
  } else {
    $(".toast").addClass('bg-success')
    $(".toast .toast-body").text('the item added succesfully')
    $(".toast").toast("show")   
    updateUserItem(productId, action);
  }
});


$(".update-cart2").on("click", function () {
  action = this.dataset.action;
  productId = this.dataset.product;
  print(user);
  if (user == "AnonymousUser") {
    print("not authenticated user");
    $(".toast").addClass('bg-info')
    $(".toast .toast-body").text('please login first to get add to cart')
    $(".toast").toast("show")
  } else {
    $(".toast").addClass('bg-success')
    $(".toast .toast-body").text('the item added succesfully')
    $(".toast").toast("show")   
    updateUserItem2(productId, action);
  }
});


function updateUserItem(productId, action) {
  var url = "/updateItem/";
  fetch(url,{
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ "productId": productId, "action": action }),
  }).then((response) => {
      return response.json();
    }).then((data) => {
      let total=data.totalCalo
      $('#cart-total').text(total)
    });
  
}
function updateUserItem2(productId, action) {
  var url = "/updateItem/";
  fetch(url,{
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ "productId": productId, "action": action }),
  }).then((response) => {
      return response.json();
    }).then((data) => {
      location.reload()
    });
  
}

/* start of search bar*/


function myFunction() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('myInput');
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  li = ul.getElementsByTagName('li');
  

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    a = li[i].getElementsByTagName("div")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}


/* end of search bar*/