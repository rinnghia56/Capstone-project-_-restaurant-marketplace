$(document).ready(function () {
    // add favorite food
    $(".add_favorite_food").on("click", function (e) {
        e.preventDefault();

        food_id = $(this).attr("data-id");
        url = $(this).attr("data-url");
        temp = $(this)
        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                if (response.status == "login_required") {
                    swal(response.message, "", "info").then(function () {
                        window.location = "/accounts/login";
                    });
                } else if (response.status == "Failed") {
                    swal(response.message, "", "error");
                } else {
                    swal(response.message, "" , "success");
                    temp.toggleClass('active')
                }
            },
        });
    });

    $(".delete_favorite_food").on("click", function(e) {
        e.preventDefault()

        food_favorite_id = $(this).attr('data-id')
        url = $(this).attr('data-url')

        $.ajax({
            type:"GET",
            url:url,
            success: function(response){
                if(response.status == "login_required"){
                    console.log('Login required')
                } else if(response.status == "Failed") {
                    swal(response.message, "", "error");
                }else {
                    swal(response.message, "" , "success");
                    document.getElementById(`food-favorite-${food_favorite_id}`).remove();
                    if(response.count_food === 0 ){
                        html = '<div class="no-food">' +
                               '<h2 class="title-no-food">You haven\'t added any favorite food yet.</h2>'+
                               '<img src="https://cdn3d.iconscout.com/3d/premium/thumb/empty-box-6219421-5102419.png" alt="">'+
                               '</div>'
                        $('.favorite-foodter').append(html)
                    }
                    
                }
            }
        })

    })
})