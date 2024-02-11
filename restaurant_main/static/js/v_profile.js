
document.addEventListener("DOMContentLoaded", function() {
    setupAutocompleteCheckOut("id_address", ".form-update", ".latitude_class", ".longitude_class", ".btn-update");
});

function setupAutocompleteCheckOut(inputId, formId, latitude_class, longitude_class, buttonSelector) {
    var addressInput = document.getElementById(inputId);

    // Khởi tạo autocomplete cho ô input
    var autocomplete = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace("value"),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: "https://nominatim.openstreetmap.org/search?format=json&q=%QUERY",
            wildcard: "%QUERY",
        },
    });

    // Thiết lập autocomplete cho ô input
    $(addressInput).typeahead(
        {
            minLength: 2,
            highlight: true,
        },
        {
            name: "address",
            display: "display_name",
            source: autocomplete,
        }
    );

    function geocode() {
        var address = addressInput.value;

        return new Promise(function(resolve, reject) {
            fetch("https://nominatim.openstreetmap.org/search?format=json&q=" + address)
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    if (data.length > 0) {
                        var lat = parseFloat(data[0].lat);
                        var lon = parseFloat(data[0].lon);
                        
                        resolve({ lat: lat, lon: lon });
                    } else {
                        reject(new Error("Không tìm thấy địa chỉ."));
                    }
                })
                .catch(function(error) {
                    reject(error);
                });
        });
    }

    document.querySelector(buttonSelector).addEventListener("click", function(event) {
        event.preventDefault();
        var form = document.querySelector(formId);
        var latitude = document.querySelector(latitude_class);
        var longitude = document.querySelector(longitude_class);

        geocode()
            .then(function(result) {
                    latitude.value = result.lat;
                    longitude.value = result.lon;
                    form.submit();
            })
            .catch(function(error) {
                swal("Not Found address", "", "error");
            });
    });
}


function checkFileUpload(id_elemnt){
    document.getElementById(id_elemnt).addEventListener('change', function(){
        if (this.files.length > 0) {
            lbl = this.previousElementSibling
            lbl.style.backgroundColor = '#1da1f2a1'
            lbl.textContent =  this.files[0].name
          }
    })
}

checkFileUpload('profile-picture-img')
checkFileUpload('cover-picture-img')
checkFileUpload('file__input')