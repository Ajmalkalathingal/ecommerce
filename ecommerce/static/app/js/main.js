    //   add to cart
    $(document).ready(function () {
        $('.add-to-cart').on('click', function (e) {
            e.preventDefault();
    
            let this_val = $(this)
            let index = this_val.attr('data-index')
    
            let productId = $('.id_' + index).val();
            let title = $('.title_' + index).val();
            let price = $('.price_' + index).text();
            let qty = $('.qty_' + index).val();
            let image = $('.image_' + index).val();
    
            console.log('ID:', productId);
            console.log('Title:', title);
            console.log('Price:', price);      
            console.log('Qty:', qty);
    
    
            $.ajax({
                url: '/add-to-cart/',
                method: 'GET', 
                data: {
                    'id': productId,
                    'title': title,
                    'price': price,
                    'qty': qty,
                    'image': image,
                },
                dataType: 'json',
                
                success: function (response) {
                  if (response.message === 'Item added to cart') {
                      console.log('Item added to cart');
                      console.log('Cart data:', response.data);
                      $('#add-to-cart').html('Item added');
                      alert('Item added to cart');
                      $('#item-count').text(response.data.cart_count);
                  } else if (response.message === 'Cart item already exists') {
                      console.log('Cart item already exists');
                      alert('Cart item already exists');
                  } else {
                      alert('Unexpected response from server');
                  }
              },
            });
        });
    });


    jQuery(document).ready(function($) {
      $('#review').submit(function(e) {
        const months_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        let date = new Date();
        let time = date.getDate() + ' ' + months_names[date.getUTCMonth()] + ',' + date.getFullYear();
        e.preventDefault();
        $.ajax({
          data: $(this).serialize(),
          method: $(this).attr('method'),
          url: $(this).attr('action'),
          dataType: 'json',
          success: function (response) {
            console.log('data saved in db..');
            if (response.bool === true) {
              $('#review-res').html('Review added');
              $('.hide-form').hide();  // Add this line to hide the review form
              $('.remove').hide();
    
              let _html = '<div class="card mb-3">';
              _html += '<div class="card-body">';
              _html += '<h5 class="card-title">' + response.context.user + '</h5>';
              _html += '<p class="card-text">' + response.context.review + '</p>';
              _html += '<div class="rating">';
              for (let i = 1; i <= response.context.rating; i++) {
                _html += '<i class="fa-sharp fa-solid fa-star text-warning"></i>';
              }
              _html += '</div>';
              _html += '<p class="card-text text-muted">' + time + '</p>';
              _html += '</div>';
              _html += '</div>';
    
              // Append the new review to the existing .comment-list
              $('.comment-list').append(_html);
            }
          }
        });
      });
    });
    

  
// remove cart and refresh cart
jQuery(document).ready(function () {
    $(".remove-button").on('click', function () {
      let productId = $(this).data('id');
      console.log(productId);
  
      // Send an AJAX request to remove the product from the cart
      $.ajax({
        url: '/remove-from-cart/',
        data: { 'id': productId },
        dataType: 'json',
        success: function (res) {
          console.log(res);
          $('#item-count').text(res.total_item);
          $('#remove-cart').html(res.data);
        }
      });
    });
  
    $(".refresh-button").on('click', function () {
      let productId = $(this).data('id');
      let newQuantity = $(this).closest('tr').find('.quantity-input').val();
      console.log(productId);
      console.log(newQuantity);
  
      // Send an AJAX request to refresh the product quantity in the cart
      $.ajax({
        url: '/refresh-from-cart/',
        data: {
          'product_id': productId,
          'product_qty': newQuantity
        },
        dataType: 'json',
        beforeSend: function () {
          console.log('sending');
        },
        success: function (res) {
          console.log(res.total_item);
          $('#item-count').text(res.total_item);
          $('#remove-cart').html(res.data);
        }
      });
    });
  });


// filter product
jQuery(document).ready(function(){
  $('.filter-checkbox, #filter-button').on('click', function(){
    console.log('clicked')

    let filter_object = {}

    let max_price = $('#max_value').attr('max')
    let min_price = $('#max_value').val()

    filter_object.max_price = parseInt(max_price)
    filter_object.min_price = parseInt(min_price)

    let filter_value = $(this).val()
    let filter_key = $(this).data('filter')
    console.log(filter_value) 
    console.log(filter_key)
    
    let checkboxs = document.querySelectorAll('input[data-filter='+ filter_key +']:checked')

    filter_object[filter_key] = Array.from(checkboxs).map(function(element){
      console.log(element)
      return element.value
    }) 

    console.log(filter_object)
    $.ajax({
      url : '/filter-products',
      data : filter_object,
      dataType : 'json',
      beforeSend : function(){
        console.log('trying to filter data')
      },
      success : function(response){
        console.log(response)
        console.log('data filter')

        $('#filterd-product').html(response.data)
      }

    })
  })
  $('#max_price').on('blur',function(){
    let min_price = $(this).attr('min')
    let max_price = $(this).attr('max')
    let current_price = $(this).val()
    console.log(max_price,min_price,current_price)

    if(current_price < parseInt(max_price) || current_price > parseInt(min_price)){
      alert('value between'+ min_price +'and'+ max_price)
    }

    return false

  })
 })

// add to wish list
jQuery(document).ready(function() {
  $(document).on('click', '.wishlist', function(e) {
    e.preventDefault();
    console.log('clicked');

    let index = $(this).attr('data-wish'); // Use data attribute to get the index

    let productId = $('.id_' + index).val();
    let title = $('.title_' + index).val();
    let price = $('.price_' + index).text();
    let qty = $('.qty_' + index).val();
    let image = $('.image_' + index).val();

    // console.log('ID:', productId);
    // console.log('Title:', title);
    // console.log('Price:', price);
    // console.log('img:', image);

    $.ajax({
      url: '/add-to-wish-list',
      data: {
        'id': productId,
        'title': title,
        'price': price,
        'image': image,
      },
      dataType: 'json',
      success: function(res) {
        console.log('response', res);
       
        if(res.data){
          console.log('check')
          $('.wishlist'+productId).find('.heart').css('color', 'red')
          $('#wishitem').text(res.data.wish_list_count)
        }
      }
    });
  });
});