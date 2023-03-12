// ok  --------------------------------------  update favorite list count
function favorite_list_status(){
    $.ajax({
        type:'GET',
        url: "/favorite/favorite_list_status/",
        success: function(res){
            $('#indicator__value').text(res);
        }

    })
}
//------------------------------------------- for running the function above all time
favorite_list_status()
// ok  --------------------------------------  add product to favorite list
function add_to_favorite(product_id){
    $.ajax({
        type:"GET",
        url:"/favorite/add_to_favorite/",
        data:{
            product_id:product_id,
        },
        success : function(res){
            $("#unlike_"+ product_id).attr("style", "color:red")
            favorite_list_status()
            alert('این محصول به لیست مورد علاقه شما افزوده شد')
        }
    })
}
// ok  --------------------------------------  delete product from favorite list
function delete_from_favorite_list(product_id){
    $.ajax({
        type:"GET",
        url:"/favorite/delete_from_favorite_list/",
        data:{
            product_id:product_id
        },
        success:function(res){
            $('#favorite_product_list').html(res)
            favorite_list_status()
            alert('این محصول از لیست مورد علاقه شما حذف شد')
        }
    })
}