// Earthquakes Custome Search
// https://earthquake.usgs.gov/earthquakes/search/


// Earthquake data link
var EarthquakeLink = "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2010-08-27%2000:00:00&endtime=2018-09-03%2023:59:59&maxlatitude=42.294&minlatitude=32.064&maxlongitude=-113.862&minlongitude=-124.893&minmagnitude=4.5&orderby=time"

// Tectonic plates link
var TectonicPlatesLink = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

// Performing a GET request to the Earthquake query URL
d3.json(EarthquakeLink, function (data) {
    // Once there is a response, sending the data.features object to the createFeatures function
    createFeatures(data.features);
});

function createFeatures(earthquakeData) {

    // Creating a GeoJSON layer containing the features array on the earthquakeData object
    // Runing the onEachFeature function once for each piece of data in the array
    var earthquakes = L.geoJson(earthquakeData, {
        onEachFeature: function (feature, layer) {
            var newDate = new Date(feature.properties.time);

            layer.bindPopup("<h3>Location: " + feature.properties.place + "<br>Magnitude: " + feature.properties.mag +
                "</h3><hr><h4>Date & Time: " + newDate + "</h4>");

            // var newYear = newDate.getFullYear()
            // console.log(newYear);
        },
       
        pointToLayer: function (feature, latlng) {
            var newDate = new Date(feature.properties.time);
            var newYear = new Date(newDate.getFullYear());
            return new L.circle(latlng,
                {   
                    radius: getRadius(feature.properties.mag),
                    fillColor: getColor(newYear),
                    fillOpacity: .7,
                    stroke: true,
                    color: "black",
                    weight: .5
                })        
        }      
    });
    
    // Sending our earthquakes layer to the createMap function
    createMap(earthquakes)
}

function createMap(earthquakes) {
    // Creating map layers
    var streetsatellitemap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets-satellite",
        accessToken: API_KEY
    });

     var streetsmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.streets",
        accessToken: API_KEY
    });

    var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.dark",
        accessToken: API_KEY
    });

    // Defining a baseMaps object to hold base layers
    var baseMaps = {
        "Satelite Map": streetsatellitemap,
        "Street Map": streetsmap,
        "Dark Map": darkmap
    };

    // Adding a tectonic plate layer
    var tectonicPlates = new L.LayerGroup();

    // Creating overlay object to hold our overlay layer
    var overlayMaps = {
        Earthquakes: earthquakes,
        "Tectonic Plates": tectonicPlates
    };

    // Creating our map, giving it the streetmap and earthquakes layers to display on load
    var myMap = L.map("map", {
        center: [37, -119],
        zoom: 5.5,
        layers: [streetsatellitemap, earthquakes, tectonicPlates]
    });

    // Adding Techtonic lines data
    d3.json(TectonicPlatesLink, function (plateData) {
        // Adding our geoJSON data, along with style information, to the tectonicplates layer.
        L.geoJson(plateData, {
            color: "red",
            weight: 3.5
        })
        .addTo(tectonicPlates);
    });

    // Creating a layer control
    // Passing in our baseMaps and overlayMaps
    // Adding the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
        collapsed: false
    }).addTo(myMap);

    // Creating legend
    var legend = L.control({ position: 'bottomright' });

    legend.onAdd = function (myMap) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
            labels = [];

        // Looping through density intervals and generate a label with a colored square for each interval
        grades.forEach((value, index) => {
            div.innerHTML +=
                '<i style="background:' + getColor(grades[index]) + '"></i> ' +
            grades[index] + (grades[index] ?'<br>' : '+');
        })
        return div;
    };

    legend.addTo(myMap);
}

function getColor(d) {
    return d > 2017 ? '#FF3333' :
        d > 2016 ? '#FF9933' :
            d > 2015 ? '#FFFF33' :
                d > 2014 ? '#99FF33' :
                    d > 2013 ? '#33FF33' :
                        d > 2012 ? '#33FFFF' :
                            d > 2011 ? '#3399FF' :
                                d > 2010 ? '#3333FF' : '#9933FF';
}

function getRadius(value) {
    return value * 10000
}