$(document).ready(function () { 
    // Add hours
    $('.add_hours').on('click',function(e){
        e.preventDefault();
        var day  = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value
        var condition;

        if(is_closed) {
            is_closed = 'True'
            condition = " day != ''"
        }else {
            is_closed = 'False'
            condition = " day != '' && from_hour != '' && to_hour != ''  "
        }

        if(eval(condition)) {
            $.ajax({
                type:'POST',
                url: url,
                data: {
                    'day':day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token
                },
                success:function(response) {
                    if(response.status == 'success'){
                        if(response.is_closed == "Closed") {
                            html = '<div class="row-content" id="hour-'+ response.id +'">'
                                        +'<div class="col-content"><p class="text">'+ response.day +'</p></div>'
                                        +'<div class="col-content"><p class="text">Closed</p></div>'
                                        +'<div class="col-content"><a href="#!" class="btn-remove remove-hour" data-url = "/accounts/vendor/opening-hours/remove/'+ response.id +'/">Remove</a></div>'+
                                        '</div>'

                            $('.table-custom').append(html)
                            document.getElementById('opening_hours').reset()
                        }else {
                            html = '<div class="row-content" id="hour-'+ response.id +'">'
                                        +'<div class="col-content"><p class="text">'+ response.day +'</p></div>'
                                        +'<div class="col-content"><p class="text">' + response.from_hour+ ' - ' + response.to_hour +'</p></div>'
                                        +'<div class="col-content"><a href="#!" class="btn-remove remove-hour" data-url = "/accounts/vendor/opening-hours/remove/'+ response.id +'/">Remove</a></div>'+
                                        '</div>'
                            $('.table-custom').append(html)
                            document.getElementById('opening_hours').reset()
                        }
                    }
                    else {
                        swal(response.message,'','error')
                    }
                }
            })
        }else {
            swal("Please fill all fields", '', 'info')
        }

    })

    // Remove hour
    $(document).on('click', '.remove-hour', function(e){
        e.preventDefault();

        let url = $(this).attr('data-url');

        $.ajax({
            'type':'GET',
            'url': url,
            'success':function(response) {
                if(response.status == 'success'){
                    document.getElementById('hour-'+response.id).remove()
                }
                else {
                    swal("Error", '', 'info')
                }
            }
        })
    })
})