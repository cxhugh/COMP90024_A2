var mymap = L.map('mapid').setView([-37.813629,144.963058], 10);
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiZnJhbmtsaTE5OTYiLCJhIjoiY2thYzljNm5xMDFsYTJwcnh1Njh5YXE2MiJ9.94jkwz8al_az0YHfcEerNw'
}).addTo(mymap);

// var popup = L.popup();

// function onMapClick(e) {
//     popup
//         .setLatLng(e.latlng)
//         .setContent("You clicked the map at " + e.latlng.toString())
//         .openOn(mymap);
// }
// mymap.on('click', onMapClick);

var population;
var baseMaps;
var overlayMaps = {};
var currentLegend;
var auth = btoa('admin:admin');
var currentLayer;
function getMapSuburbTotal() {
    var suburb = [];
    $.ajax({
        url:'http://172.26.129.233:5984/aurin_result/sa2_map_aurin_data',
        dataType:'json',
        async : true,
        xhrFields:{withCredentials:true},
        headers: {"Authorization": "Basic " + auth},
        crossDomain:true,
        success:function(data){    
            suburb = data;
            population = L.geoJSON(suburb, {
                style: style,
                onEachFeature: onEachFeature
            }).addTo(mymap); 

            income = L.geoJSON(suburb, {
                style: style_income,
                onEachFeature: onEachFeature
            }); 

            education = L.geoJSON(suburb, {
                style: style_edu,
                onEachFeature: onEachFeature
            }); 

            unemployed = L.geoJSON(suburb, {
                style: style_emply,
                onEachFeature: onEachFeature
            }); 
            
            baseMaps = {
                "Population": population,
                "Education": education,
                "Unemployed": unemployed,
                "Income": income
            };
            L.control.layers(baseMaps,overlayMaps,{
                collapsed: false,
                position: 'bottomleft'
            }).addTo(mymap);
        },
        error:function(data){
            console.log('request failed')
        }
    });
}

function getColor(d) {
    return d > 7000  ? '#800026' :
           d > 5000  ? '#BD0026' :
           d > 4000  ? '#E31A1C' :
           d > 2000  ? '#FC4E2A' :
           d > 1000   ? '#FD8D3C' :
           d > 500   ? '#FEB24C' :
           d > 300   ? '#FED976' :
                      '#FFEDA0';
}

function getColor_income(d) {
    return d > 1800  ? '#800026' :
           d > 1500  ? '#BD0026' :
           d > 1300  ? '#E31A1C' :
           d > 1100  ? '#FC4E2A' :
           d > 900   ? '#FD8D3C' :
           d > 700   ? '#FEB24C' :
           d > 500   ? '#FED976' :
                      '#FFEDA0';
}

function getColor_edu(d) {
    return d > 35  ? '#800026' :
           d > 30  ? '#BD0026' :
           d > 25  ? '#E31A1C' :
           d > 20  ? '#FC4E2A' :
           d > 15  ? '#FD8D3C' :
           d > 10  ? '#FEB24C' :
           d > 5   ? '#FED976' :
                      '#FFEDA0';
}

function getColor_eply(d) {
    return d > 20  ? '#800026' :
           d > 15  ? '#BD0026' :
           d > 10  ? '#E31A1C' :
           d > 8   ? '#FC4E2A' :
           d > 6   ? '#FD8D3C' :
           d > 4   ? '#FEB24C' :
           d > 2   ? '#FED976' :
                      '#FFEDA0';
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.population_density),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function style_income(feature) {
    return {
        fillColor: getColor_income(feature.properties.equivalised_household_income_median),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function style_edu(feature) {
    return {
        fillColor: getColor_edu(feature.properties.degree_diploma_certificate_percent),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function style_emply(feature) {
    return {
        fillColor: getColor_eply(feature.properties.unemployed_percent),
        weight: 2,
        opacity: 1,
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
        fillOpacity: 0.8
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }

    if (currentLayer == "Population"){
        info.update(layer.feature.properties);
    }
    else if (currentLayer == "Income"){
        info_ic.update(layer.feature.properties);
    }
    else if (currentLayer == "Education"){
        info_ed.update(layer.feature.properties);
    }
    else if (currentLayer == "Unemployed"){
        info_ep.update(layer.feature.properties);
    }
}

function resetHighlight(e) {
    population.resetStyle(e.target);
    if (currentLayer == "Population"){
        info.update();
    }
    else if (currentLayer == "Income"){
        info_ic.update();
    }
    else if (currentLayer == "Education"){
        info_ed.update();
    }
    else if (currentLayer == "Unemployed"){
        info_ep.update();
    }
}

// function zoomToFeature(e) {
//     mymap.fitBounds(e.target.getBounds());
// }

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight
        // click: zoomToFeature
    });
}

var info = L.control();
info.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
info.update = function (props) {
    this._div.innerHTML = '<h4>Population Density</h4>' +  (props ?
        '<b>' + props.SA2_NAME16 + '</b><br />' + props.population_density + ' people / km<sup>2</sup>'
        : 'Greater Melbourne');
};

var info_ic = L.control();
info_ic.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
info_ic.update = function (props) {
    this._div.innerHTML = '<h4>Average Income</h4>' +  (props ?
        '<b>' + props.SA2_NAME16 + '</b><br />' + props.equivalised_household_income_median + ' dollars / week'
        : 'Greater Melbourne');
};

var info_ed = L.control();
info_ed.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
// method that we will use to update the control based on feature properties passed
info_ed.update = function (props) {
    this._div.innerHTML = '<h4>Education Level</h4>' +  (props ?
        '<b>' + props.SA2_NAME16 + '</b><br />' + props.degree_diploma_certificate_percent + '% has doploma degree'
        : 'Greater Melbourne');
};

var info_ep = L.control();
info_ep.onAdd = function (mymap) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};
info_ep.update = function (props) {
    this._div.innerHTML = '<h4>Unemployed rate</h4>' +  (props ?
        '<b>' + props.SA2_NAME16 + '</b><br />' + props.unemployed_percent + '%'
        : 'Greater Melbourne');
};

// legeng
var legend = L.control({position: 'bottomright'});
legend.onAdd = function (mymap) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 300, 500, 1000, 2000, 4000, 5000, 7000],
        labels = [];
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};

var income_legend =  L.control({position: 'bottomright'});
income_legend.onAdd = function (mymap) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 500, 700, 900, 1100, 1300, 1500, 1800],
        labels = [];
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_income(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};

var edu_legend =  L.control({position: 'bottomright'});
edu_legend.onAdd = function (mymap) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 5, 10, 15, 20, 25, 30, 35],
        labels = [];
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_edu(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};

var emply_legend =  L.control({position: 'bottomright'});
emply_legend.onAdd = function (mymap) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 2, 4, 6, 8, 10, 15, 20],
        labels = [];
    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor_eply(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }
    return div;
};
getMapSuburbTotal()

legend.addTo(mymap);
info.addTo(mymap);
currentLayer = "Population";
currentLegend = legend;
currentInfo = info;

mymap.on('baselayerchange', function (eventLayer) {
    if (eventLayer.name == 'Income') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);
        currentLegend = income_legend;
        currentInfo = info_ic;
        currentLayer = "Income";
        income_legend.addTo(mymap);
        info_ic.addTo(mymap);
    }
    else if  (eventLayer.name == 'Population') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);
        currentLegend = legend;
        currentInfo = info;
        currentLayer = "Population";
        legend.addTo(mymap);
        info.addTo(mymap);
    }
    else if  (eventLayer.name == 'Education') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);
        currentLegend = edu_legend;
        currentInfo = info_ed;
        currentLayer = "Education";
        edu_legend.addTo(mymap);
        info_ed.addTo(mymap);
    }
    else if  (eventLayer.name == 'Unemployed') {
        mymap.removeControl(currentLegend);
        mymap.removeControl(currentInfo);
        currentLegend = emply_legend;
        currentInfo = info_ep;
        currentLayer = "Unemployed";
        emply_legend.addTo(mymap);
        info_ep.addTo(mymap);
    }
})





  


