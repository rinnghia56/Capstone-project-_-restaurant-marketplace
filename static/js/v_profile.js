
document.addEventListener("DOMContentLoaded", function() {
    setupAutocompleteCheckOut("id_address", "form-checkout", "id_latitude_checkout", "id_longitude_checkout", ".btn-place-order");
});

function setupAutocompleteCheckOut(inputId, formId, latitudeId, longitudeId, buttonSelector) {
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

    // document.querySelector(buttonSelector).addEventListener("click", function(event) {
    //     event.preventDefault();
    //     // var form = document.getElementById(formId);
    //     // var latitude = document.getElementById(latitudeId);
    //     // var longitude = document.getElementById(longitudeId);

    //     geocode()
    //         .then(function(result) {
    //                 // form.submit();
    //         })
    //         .catch(function(error) {
    //             swal("Not Found address", "", "error");
    //         });
    // });
}
