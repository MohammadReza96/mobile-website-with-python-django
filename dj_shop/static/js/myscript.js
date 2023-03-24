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
});
// ok ------------------------------------- for showing the reply box for 1 comment
function showCreateCommentForm(comment_id,product_slug){
    $.ajax({
        type:"GET",
        url:"/comments/create_comment/" + product_slug,
        data:{
            comment_id:comment_id
        },
        success:function(res){
            $('#btn_'+ comment_id).hide();  // for hide a tag in html
            $('#comment_form_'+ comment_id).show();
            $('#btn_unshow_'+ comment_id).text('انصراف');
            $("#comment_form_"+comment_id).html(res)
        }
    });
}
// ok ------------------------------------- for hiding the reply box for 1 comment
function UnshowCreateCommentForm(comment_id){
    $('#btn_'+ comment_id).show();
    $('#btn_unshow_'+ comment_id).text('');
    $('#comment_form_'+ comment_id).hide();
}
// ok ------------------------------------- for setting a score for a product
function addScore(score,product_id){
    var starRating=document.querySelectorAll('.fa-star')
    starRating.forEach(element =>{
        element.classList.remove('checked')
    })
    for (let i =1 ; i <= score ; i++){
        const element = document.getElementById('star_' + i);
        element.classList.add('checked')
    }

    $.ajax({
        type: "GET",
        url: "/scoring/user_score/",
        data:{
            product_id:product_id,
            score:score
        },
        success : function(res){
            // alert(res)
        }
    });

    starRating.forEach(element=>{
        element.classList.add('disable')
    })
}
// not completed -------------------------- for updating average score
// function average_Score_status(product_id){
//     $.ajax({
//         type:'GET',
//         data:{
//             product_id:product_id
//         },
//         url: "/scoring/average_score_update/",
//         success: function(res){
//             $('#indicator__value').text(res);
//         }

//     })
// }
