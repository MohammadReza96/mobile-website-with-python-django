// ok  -------------------------------------- for checking user_name is valid or not 
$(document).ready(function(){
    $('#user_name_check').blur(function(event){
        let user_name = $('#user_name_check').val()
        $.ajax({
            type:"GET",
            url:"/accounts/username_form_validation/",
            data:{
                user_name:user_name
            },
            success:function(res){
                if (user_name == "") {
                    $("#register_form_message").text('').css({"border":"0px solid white"})
                }else if(res == 'ok'){
                    $("#register_form_message").text('نام کاربری معتبر است').css({"color":"green","border":"1px solid green"})
                }
                else {
                    $("#register_form_message").text('این نام کاربری قبلا استفاده شده است').css({"color":"red","border":"1px solid red"})
                }
            }
        })
    })
})
// ok  -------------------------------------- update favorite list count
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
// ok  -------------------------------------- add product to favorite list
function add_to_favorite(product_id){
    $.ajax({
        type:"GET",
        url:"/favorite/add_to_favorite/",
        data:{
            product_id:product_id,
        },
        success : function(res){
            $("#unlike_"+ product_id).attr("style", "color:red;")
            favorite_list_status()
            alert(res)
        }
    })
}
// ok  -------------------------------------- delete product from favorite list
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
// ok  -------------------------------------- changing warehouse_status color
$(document).ready(function(){
    function change_color_warehouse_status_red(){
        $(".warehouse_status").css("color","red")
    }
    function change_color_warehouse_status_white(){
        $(".warehouse_status").css("color","#BBBBBB")
    }
    setInterval(change_color_warehouse_status_red,700)
    setInterval(change_color_warehouse_status_white,2200)
})


