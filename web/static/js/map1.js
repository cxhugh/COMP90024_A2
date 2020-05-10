var heatmapData = [
  new google.maps.LatLng(-25.921984, 134.418261),
  new google.maps.LatLng(-25.916532, 134.423332),
  new google.maps.LatLng(-25.930658, 134.419787),
  new google.maps.LatLng(-21.930658, 128.419787),
  new google.maps.LatLng(-20.782, 122.419787),
  new google.maps.LatLng(-16.782, 112.419787),
  new google.maps.LatLng(-11.782, 135.419787),
  new google.maps.LatLng(-27.785, 166.419787),
  new google.maps.LatLng(-22.785, 125.419787),
  new google.maps.LatLng(-25.785, 122.419787),
  new google.maps.LatLng(-27.785, 130.419787),
  new google.maps.LatLng(-29.785, 151.419787),
  new google.maps.LatLng(-24.785, 141.419787),
  new google.maps.LatLng(-24.785, 144.419787),
    new google.maps.LatLng(-22.930658, 134.419787),
  new google.maps.LatLng(-21.930658, 128.419787),
  new google.maps.LatLng(-24.782, 122.419787),
  new google.maps.LatLng(-16.782, 112.419787),
  new google.maps.LatLng(-16.782, 135.419787),
  new google.maps.LatLng(-28.785, 166.419787),
  new google.maps.LatLng(-24.785, 125.419787),
  new google.maps.LatLng(-23.785, 127.419787),
  new google.maps.LatLng(-27.785, 134.419787),
  new google.maps.LatLng(-29.785, 141.419787),
  new google.maps.LatLng(-28.785, 131.419787),
  new google.maps.LatLng(-24.785, 154.419787)
];

var sanFrancisco = new google.maps.LatLng(-25.799891182088306,134.296875);

map = new google.maps.Map(document.getElementById('main-abcd'), {
  center: sanFrancisco,
  zoom: 4,
    // disableDefaultUI:true,
  mapTypeId: 'roadmap'
});

var heatmap = new google.maps.visualization.HeatmapLayer({
  data: heatmapData
});
heatmap.setMap(map);

var overlay;
USGSOverlay.prototype = new google.maps.OverlayView();


  var bounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(-25.281819, 134.287132),
      new google.maps.LatLng(-25.400471, 134.005608));

  // The photograph is courtesy of the U.S. Geological Survey.
  var srcImage =new GCL();

  // The custom USGSOverlay object contains the USGS image,
  // the bounds of the image, and a reference to the map.
  overlay = new USGSOverlay(bounds, srcImage, map);
