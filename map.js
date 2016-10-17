var map;
var geocoder;
var markers = [];
var destinationMark;

// display all marks when csv file uploaded
$(document).ready(function() {
  $('#csv').bind('change', handleFileSelect);
});

// initialize map
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 48.1351, lng: 11.5820},
    zoom: 11
  });
  geocoder = new google.maps.Geocoder();

  // mark the destination
  markDestination();

  $('#university').on('change', function (event) {
      // var optionSelected = $("option:selected", this);
      // var valueSelected = this.value;
      destinationMark.setMap(null);
      markDestination();
  });
}

// TODO: make destination mark icon differently
function markDestination() {

  geocoder.geocode({'address': $('select[name=university]').val()}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      console.log(results[0].geometry.location)
      destinationMark = new google.maps.Marker({
            map: map,
            position: results[0].geometry.location,
            animation: google.maps.Animation.DROP
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

// hanlder for file select
function handleFileSelect(evt) {

  // read the csv file
  var files = evt.target.files;
  var file = files[0];
  var reader = new FileReader();
  reader.readAsText(file);

  // loading handler
  reader.onload = function(event) {

    var csv = event.target.result;
    var data = $.csv.toArrays(csv);

    // appear time
    var i = 0;

    // processing all street address
    for(var row in data) {

      if (data[row][7] != $('select[name=room-num]').val()) continue;

      // make housing information as a js object
      var infos = {
        'longitude': data[row][0],
        'latitude': data[row][1],
        'address': data[row][3],
        'rent': data[row][10],
        'room-num': data[row][7],
        'start': data[row][12],
        'end': data[row][13],
        'notes': data[row][19],
        'url': data[row][20]
      };

      // geocoding
      addMarks(infos, map, i);
      i += 200;
    }
  }
}

// TODO: calculate the arrive time from location to destination
// TODO: show directions

function addMarks(infos, resultsMap, timeout) {

  var content = '\
  <div id="content"> \
    <h4>'+infos['address']+'</h4>\
    <h5>Start from: <small>'+infos['start']+'</small></h5>\
    <h5>End at: <small>'+infos['end']+'</small></h5>\
    <h5>Total rent: <small>'+infos['rent']+'</small></h5>\
    <h6>Notes: <small>'+infos['notes']+'</small></h6>\
    <a href="http://www.studentenwerk-muenchen.de'+infos['url']+'">Go for Contact\
    <span class="glyphicon glyphicon-link" aria-hidden="true"></span></a>\
  </div>'

  var infowindow = new google.maps.InfoWindow({
    content: content,
    maxWidth: 200,
  });

  // add mark to the map
  window.setTimeout(function() {

    // generate the mark
    var marker = new google.maps.Marker({
      map: resultsMap,
      position: {lat: parseFloat(infos['longitude']), lng: parseFloat(infos['latitude'])},
      animation: google.maps.Animation.DROP
    });

    // show housing information when mark clicked
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    })
    markers.push(marker);

  }, timeout);


}
