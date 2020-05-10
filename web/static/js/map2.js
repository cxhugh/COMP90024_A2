     function getPageTotalAndDataTotal() {

    var pageTotal = [];
            $.ajax({
        url:'http://172.26.129.233:5984/view_results/coord_count_geojson',
        dataType:'json',
       async : false,
                xhrFields:{
        withCredentials:true
            },
            crossDomain:true,
        success:function(data){
        pageTotal = data;

        },
        error:function(data){
            console.log('请求失败')
        }
    });
    return pageTotal;
}
    var lii = getPageTotalAndDataTotal();


      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: {lat: -33.865427, lng: 151.196123},
          mapTypeId: 'roadmap'
        });

          map.data.addGeoJson(lii);

        map.data.setStyle(function(feature) {
          var magnitude = feature.getProperty('count');
          return {
            icon: getCircle(magnitude)
          };
        });



      }

      function getCircle(magnitude) {
        return {
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: 'red',
          fillOpacity: .2,
          scale:   6,                              //Math.pow(2,magnitude)/2,
          strokeColor: 'white',
          strokeWeight: .5
        };
      }