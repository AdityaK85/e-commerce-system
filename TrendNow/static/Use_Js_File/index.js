function add_to_cart(id) {
  prod_qty = "1"
  console.log("click")


  $.ajax({
    method: "POST",
    url: "/add_to_cart_home/",
    data: {
      'item_id': id,
      prod_qty
    },
    success: function (response) {
      console.log(response)
      if (response == "added") {
        iziToast.show({
          title: "Product Added To Your Cart ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });

      } else if (response == "Alerdy added") {
        iziToast.show({
          title: "Product Already Added Check Your Cart ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      } else if (response == "quatity high") {
        iziToast.show({
          title: "Product Quantity Too high ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      } else if (response == "1") {
        iziToast.show({
          title: "Try Again Later !",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      }
    }
  });
};



function wishlist(id) {

  $.ajax({
    method: "POST",
    url: "/add_to_wishlist/",
    data: {
      item_id: id,
    },
    success: function (response) {
      console.log(response);
      if (response == "added") {
        iziToast.show({
          title: "Product Added To Your Wishlist ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });

      } else if (response == "already add") {
        iziToast.show({
          title: "Product Already Added ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      } else if (response == "not added") {
        iziToast.show({
          title: "Product Not Added ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      } else if (response == "Product not found") {
        iziToast.show({
          title: "Product Not Found ",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      } else if (response == "1") {
        iziToast.show({
          title: "Try Again Later !",
          message: "! Shop More With Trend",
          position: "bottomLeft",
        });
      }
    },
  });
}

// Perfect run wishlist code do touch 


function get_id(id) {
  $.ajax({
    method: "POST",
    url: "/payment/",
    data: {
      'item_id': id,
    }, success: function (response) {
      console.log(response)
    }
  })
}