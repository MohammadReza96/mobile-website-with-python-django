// ok  --------------------------------------  add_product_to_favorite
function add_to_favorite(product_id){
    $.ajax({
        type:"GET",
        url:"/favorite/add_to_favorite/",
        data:{
            product_id:product_id,
        },
        success : function(res){
            $("#unlike_"+ product_id).attr("style", "color:red")
        }
    })
}