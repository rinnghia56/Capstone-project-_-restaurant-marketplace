function openModal(modalId) {
    var modal = document.querySelector(`.${modalId}`);
    modal.style.display = "flex";
}

function closeModal(modalId) {
    var modal = document.querySelector(`.${modalId}`);
    modal.style.display = "none";
}


document.addEventListener("DOMContentLoaded", function() {
    setupAutocomplete("address_search_heading", "search_form_address", "id_latitude", "id_longitude", ".btn-search-2");
    setupAutocomplete("address_search_heading_2", "search_form_address_2", "id_latitude_2", "id_longitude_2", ".btn-search-3");
});

function setupAutocomplete(inputId, formId, latitudeId, longitudeId, buttonSelector) {
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
        var form = document.getElementById(formId);
        var latitude = document.getElementById(latitudeId);
        var longitude = document.getElementById(longitudeId);

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


document.addEventListener("DOMContentLoaded", function () { 
    var latInput = document.getElementById('your_latitude');
    var lngInput = document.getElementById('your_longitude');
    var location_btn = document.getElementById('location-btn');
    var form = document.querySelector(".your-location");

    location_btn.addEventListener('click', function(){
        navigator.geolocation.getCurrentPosition(function(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
      
        // Gán giá trị vào input
        latInput.value = latitude;
        lngInput.value = longitude;
        form.submit()
      });
    })

})
