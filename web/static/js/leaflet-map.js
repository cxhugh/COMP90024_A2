
var mymap = L.map('map1').setView([-30,135], 4);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoiamlhbnhpbnh1IiwiYSI6ImNrYWM2OGtmcDAxeG4zMHA2bmdjYXNscmkifQ.tyW3dKaenLGHgXAHRPvWvg ', {
	     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(mymap);

//	var geojson = L.geoJson(statesData).addTo(mymap);








 var LeafIcon = L.Icon.extend({
    options: {
        iconSize:     [20, 20],
        iconAnchor:   [22, 22],
        popupAnchor:  [-3, -76]
    }
});

// add icon of sentiment
var posIcon = new LeafIcon({iconUrl: '../static/img/pos.png'}),
    negIcon = new LeafIcon({iconUrl: '../static/img/neg.png'}),
    neuIcon = new LeafIcon({iconUrl: '../static/img/neu.png'});


var cities = L.layerGroup();
var cities1 = L.layerGroup();


var auth = btoa('admin:admin');
    $.ajax({
        url:'http://172.26.134.56:5984/aurin_result/alcohol_sentiment',
        dataType:'json',
        async : true,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            data1=data.data;
        //      console.log(data);
            for (var key in data1){

                var state_alcohol = data1[key];

                // console.log(mel_suburb)
              add_sentiment_icon(state_alcohol['center'],state_alcohol['value'])
           }
            // add_sentiment_icon()
        },
        error:function(data){
            console.log('request sentiment failed')
        }
    });
    $.ajax({
        url:'http://172.26.134.56:5984/aurin_result/alltopic_sentiment',
        dataType:'json',
        async : true,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            data1=data.data;
        //       console.log(data);
            for (var key in data1){

                var state_topic = data1[key];

                // console.log(mel_suburb)
              add_sentiment_icon1(state_topic['center'],state_topic['value'])
           }
            // add_sentiment_icon()
        },
        error:function(data){
            console.log('request sentiment failed')
        }
    });

function add_sentiment_icon(point,value){
    if (value > 0.05){
        L.marker(point, {icon: posIcon}).addTo(cities);
    }
    else if (value < -0.05){
        L.marker(point, {icon: negIcon}).addTo(cities);
    }
    else{
        L.marker(point, {icon: neuIcon}).addTo(cities);
    }
}

function add_sentiment_icon1(point,value){
    if (value > 0.05){
        L.marker(point, {icon: posIcon}).addTo(cities1);
    }
    else if (value < -0.05){
        L.marker(point, {icon: negIcon}).addTo(cities1);
    }
    else{
        L.marker(point, {icon: neuIcon}).addTo(cities1);
    }
}


var population;
var baseMaps;
var overlayMaps = {	"Alcohol Average Sentiment": cities,
                        "Topic Average Sentiment": cities1,};
var currentLegend;
var currentLayer;
var currentInfo;


function getMapAusTotal() {
    var aus = [];
    $.ajax({
        url:'http://172.26.134.56:5984/aurin_result/state_map_twitter_data',
        dataType:'json',
        async : true,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){
            aus = data;
             population = L.geoJSON(aus, {
                style: styleP,
            onEachFeature: onEachFeature
            }).addTo(mymap);
                topic = L.geoJson(aus, {style: styleT,
                    onEachFeature: onEachFeature
                });
                   alcohol = L.geoJson(aus, {style: styleA,
                        onEachFeature: onEachFeature
                    });

            baseMaps = {
              "Population": population,
              "Topic": topic,
                  "Alcohol": alcohol

                };

            L.control.layers(baseMaps, overlayMaps, {
                collapsed:false,
                position:'bottomleft'
            }).addTo(mymap);

         //   console.log(aus)
        },
        error:function(data){
            console.log('request failed')
        }
    });

}



//getMapAusTotal()



function getColorP(d) {
    return d > 8000000  ? '#800026' :
           d > 7000000  ? '#BD0026' :
           d > 6000000  ? '#E31A1C' :
           d > 5000000  ? '#FC4E2A' :
           d > 4000000   ? '#FD8D3C' :
           d > 2000000   ? '#FEB24C' :
           d > 1000000   ? '#FED976' :
                      '#FFEDA0';
}

function styleP(feature) {
    return {
        fillColor: getColorP(feature.properties.state_population),
        weight: 2,
        opacity: 0.5,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function getColorT(d) {
    return d > 70000  ? '#800026' :
           d > 60000  ? '#BD0026' :
           d > 50000  ? '#E31A1C' :
           d > 40000  ? '#FC4E2A' :
           d > 30000  ? '#FD8D3C' :
           d > 20000   ? '#FEB24C' :
           d > 10000  ? '#FED976' :
                      '#FFEDA0';
}

function styleT(feature) {
    return {
        fillColor: getColorT(feature.properties.alltopic_count),
        weight: 2,
        opacity: 0.5,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}
    function getColorA(d) {
    return d > 7000  ? '#800026' :
           d > 6000  ? '#BD0026' :
           d > 5000  ? '#E31A1C' :
           d > 4000  ? '#FC4E2A' :
           d > 3000   ? '#FD8D3C' :
           d > 2000   ? '#FEB24C' :
           d > 1000   ? '#FED976' :
                      '#FFEDA0';
}

function styleA(feature) {
    return {
        fillColor: getColorA(feature.properties.alcohol_count),
        weight: 2,
        opacity: 0.5,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}



// mouse on hover highlight
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 2,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          layer.bringToFront();
    }
		    if (currentLayer === "Population"){
        infoP.update(layer.feature.properties);
    }
    else if (currentLayer === "Topic"){
        infoT.update(layer.feature.properties);
    }
    else if (currentLayer === "Alcohol"){
        infoA.update(layer.feature.properties);
    }
}


function resetHighlight(e) {
    if (currentLayer === "Population"){
        population.resetStyle(e.target);
        infoP.update();
    }
    else if (currentLayer === "Topic"){
        topic.resetStyle(e.target);
        infoT.update();
    }
    else if (currentLayer === "Alcohol"){
        alcohol.resetStyle(e.target);
        infoA.update();
    }
}


function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight

    });
}


var infoP = L.control();
        infoP.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
infoP.update = function (props) {
    this._div.innerHTML = '<h2>The Population of Australia</h2>' +  (props ?
        '<b><h3>' + props.STATE_NAME + '</h3></b>' + '<b>'+props.state_population +'</b>'+ ' in Total '
        : 'Hover over a state');
};

var infoT = L.control();
infoT.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
infoT.update = function (props) {
    this._div.innerHTML = '<h2>All topics in twitter</h2>' +  (props ?
        '<b><h3>' + props.STATE_NAME + '</h3></b><b>' + props.alltopic_count +'</b> in Total'+
         '<br/>Average sentiment of all topics ' + ' is <b>'+props.alltopic_sentiment_avg.toFixed(3) +'</b>'+
        '<br/>The Population of ' +props.STATE_NAME+' is <b>'+ props.state_population+'</b>'
        : 'Hover over a state');
};

var infoA = L.control();
infoA.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
infoA.update = function (props) {
    this._div.innerHTML = '<h2>The number of alcohol</h2>' +  (props ?
        '<b><h3>' + props.STATE_NAME + '</h3></b><b>' + props.alcohol_count + '</b>  in Total'+
           '<br/>Average sentiment of people to alcohol ' +' is <b>' +props.alcohol_sentiment_avg.toFixed(3) +'</b>'+
        '<br/>The Population of ' +props.STATE_NAME+' is <b>'+ props.state_population+'</b>'
        : 'Hover over a state');
};


var legendP = L.control({position: 'bottomright'});

	legendP.onAdd = function (mymap) {

		var div = L.DomUtil.create('div', 'info legend'),
			grades = [0, 1000000, 2000000, 4000000, 5000000, 6000000, 7000000, 8000000],
			labels = [];

    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorP(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
		return div;
	};

		var legendT = L.control({position: 'bottomright'});

	legendT.onAdd = function (mymap) {

		var div = L.DomUtil.create('div', 'info legend'),
			grades = [0,10000, 20000, 30000, 40000, 50000, 60000, 70000],
			labels = [];

    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorT(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
		return div;
	};

		var legendA = L.control({position: 'bottomright'});

	legendA.onAdd = function (mymap) {

		var div = L.DomUtil.create('div', 'info legend'),
			grades = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000],
			labels = [];

    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColorA(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
		return div;
	};


//   legend.addTo(mymap);
getMapAusTotal();

legendP.addTo(mymap);
infoP.addTo(mymap);
currentLayer = "Population";
currentLegend = legendP;
currentInfo = infoP;

mymap.on('baselayerchange', function (eventLayer) {
    if (eventLayer.name === 'Population') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);

        currentInfo = infoP;
        currentLegend = legendP;
        currentLayer = "Population";

        legendP.addTo(mymap);
        infoP.addTo(mymap);
    } else if (eventLayer.name === 'Topic') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);


        currentInfo = infoT;

        currentLegend = legendT;
        currentLayer = "Topic";

        legendT.addTo(mymap);
        infoT.addTo(mymap);
    }
    else if (eventLayer.name === 'Alcohol') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);

        currentLegend = legendA;
        currentInfo = infoA;
        currentLayer = "Alcohol";

        legendA.addTo(mymap);
        infoA.addTo(mymap);
    }
  })




