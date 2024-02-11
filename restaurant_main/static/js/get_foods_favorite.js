$(document).ready(
    function(){
        $.ajax({
            type:"GET",
            url:"/marketplace/get_foods_favorite/",
            success:function(response){
                if (response.status == "login_required") {
                    console.log("Login required")
                } else if (response.status == "Failed") {
                    console.log("Fail")
                } else {
                    response.id_food.forEach((item) => {
                      $(`#food-item-${item} .add_favorite_food`).addClass('active')
                    })
                }
            }
        })
    }
)