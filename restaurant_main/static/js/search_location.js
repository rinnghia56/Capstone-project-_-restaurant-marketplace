document.addEventListener("DOMContentLoaded", function () {
var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

var fullscreenControl = L.control.fullscreen();
map.addControl(fullscreenControl);

var latitude_element = document.querySelector('.latitude_element')
var longitude_element = document.querySelector('.longitude_element')

var latitude = latitude_element.getAttribute('data-lat');
var longitude = longitude_element.getAttribute('data-long');

var positionElement = document.getElementById("position_restaurant");
var positionData = positionElement.getAttribute("data-position");

positionData = positionData.replaceAll("'",'"')
console.log(JSON.parse(positionData))

var marker;

function reverseGeocode(latitude, longitude) {
  var addressOutput = document.getElementById('your_location');

  var lat = parseFloat(latitude);
  var lon = parseFloat(longitude);

  if (marker) {
    map.removeLayer(marker);
  }

  marker = L.marker([lat, lon]).addTo(map);
  map.setView([lat, lon], 13);

  var locations = JSON.parse(positionData)

  var markers = [];

  locations.forEach(function(location) {
    var lat = parseFloat(location.latitude);
    var lon = parseFloat(location.longitude);
    var address = location.address;
    var restaurant_name = location.restaurant_name;

    var redIcon = L.icon({
      iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
    });

    var marker = L.marker([lat, lon], { icon: redIcon }).addTo(map);
    marker.bindPopup(restaurant_name + " | " + address); 
    markers.push(marker);
  });

  var group = new L.featureGroup(markers);
  map.fitBounds(group.getBounds());

  fetch('https://nominatim.openstreetmap.org/reverse?format=json&lat=' + lat + '&lon=' + lon)
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      if (data.address) {
        var address = data.display_name;
        marker.bindPopup('Vị trí của bạn: ' + address);
        addressOutput.textContent = 'Địa chỉ: ' + address;
      } else {
        addressOutput.textContent = 'Không tìm thấy địa chỉ.';
      }
    })
    .catch(function(error) {
      console.log('Lỗi: ', error);
    });
}

function distance_map() {
  var waypoints = [];
  var routingControl;
  var markersLayer = L.layerGroup().addTo(map);

  function onMapClick(e) {
      if (waypoints.length >= 2) {
          clearMap();
      }

      waypoints.push(e.latlng);
      L.marker(e.latlng, { icon: createCustomIcon() }).addTo(markersLayer);

      if (waypoints.length > 1) {
          createRoute();
      }
  }

  function createRoute() {
      var waypointsCopy = waypoints.slice(); // Tạo một bản sao của danh sách waypoints

      routingControl = L.Routing.control({
          waypoints: waypointsCopy,
          routeWhileDragging: true,
          lineOptions: {
            styles: [{ color: 'red', opacity: 1, weight: 4 }]
          }
      }).addTo(map);
  }


  function createCustomIcon() {
    // Tạo biểu tượng đánh dấu tùy chỉnh với màu vàng
    var customIcon = L.icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41]
    });

    return customIcon;
}


  function clearMap() {
      map.removeControl(routingControl);
      routingControl = null;

      markersLayer.clearLayers();

      waypoints = [];
  }

  map.on('click', onMapClick);
}


reverseGeocode(latitude, longitude)
distance_map()

})