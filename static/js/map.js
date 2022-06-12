window.addEventListener("load", function () {
  console.log("loaded");

  var baseMaps = {
    OpenStreetMap: osm,
    "Mapbox Streets": streets,
  };

  var overlayMaps = {
    Cities: cities,
  };
  var geojsonFeature = {
    type: "Feature",
    properties: {
      name: "Coors Field",
      amenity: "Baseball Stadium",
      popupContent: "This is where the Rockies play!",
    },
    geometry: {
      type: "Point",
      coordinates: [-104.99404, 39.75621],
    },
  };

  var map = L.map("map").setView([-21.066017, 28.457861], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© Lims",
  }).addTo(map);

  var marker = L.marker([51.5, -0.09]).addTo(map);
  var polygon = L.polygon([
    [51.509, -0.08],
    [51.503, -0.06],
    [51.51, -0.047],
  ]).addTo(map);

  marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();
  polygon.bindPopup("I am a polygon.");
  var popup = L.popup()
    .setLatLng([51.513, -0.09])
    .setContent("I am a standalone popup.")
    .openOn(map);
  L.geoJSON(geojsonFeature).addTo(map);

  var states = [
    {
      type: "Feature",
      properties: { party: "Republican" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [-104.05, 48.99],
            [-97.22, 48.98],
            [-96.58, 45.94],
            [-104.03, 45.94],
            [-104.05, 48.99],
          ],
        ],
      },
    },
    {
      type: "Feature",
      properties: { party: "Democrat" },
      geometry: {
        type: "Polygon",
        coordinates: [
          [
            [-109.05, 41.0],
            [-102.06, 40.99],
            [-102.03, 36.99],
            [-109.04, 36.99],
            [-109.05, 41.0],
          ],
        ],
      },
    },
  ];

  L.geoJSON(states, {
    style: function (feature) {
      switch (feature.properties.party) {
        case "Republican":
          return { color: "#ff0000" };
        case "Democrat":
          return { color: "#0000ff" };
      }
    },
  }).addTo(map);

  var littleton = L.marker([39.61, -105.02]).bindPopup(
      "This is Littleton, CO."
    ),
    denver = L.marker([39.74, -104.99]).bindPopup("This is Denver, CO."),
    aurora = L.marker([39.73, -104.8]).bindPopup("This is Aurora, CO."),
    golden = L.marker([39.77, -105.23]).bindPopup("This is Golden, CO.");

  var cities = L.layerGroup([littleton, denver, aurora, golden]);
  var osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: "© Lims",
  });

  var streets = L.tileLayer(mapboxUrl, {
    id: "mapbox/streets-v11",
    tileSize: 512,
    zoomOffset: -1,
    attribution: mapboxAttribution,
  });

  var map = L.map("map", {
    center: [39.73, -104.99],
    zoom: 10,
    layers: [osm, cities],
  });

  //controls

  var layerControl = L.control.layers(baseMaps, overlayMaps).addTo(map);
  var baseMaps = {
    "<span style='color: gray'>Grayscale</span>": grayscale,
    Streets: streets,
  };

  var crownHill = L.marker([39.75, -105.09]).bindPopup(
      "This is Crown Hill Park."
    ),
    rubyHill = L.marker([39.68, -105.0]).bindPopup("This is Ruby Hill Park.");

  var parks = L.layerGroup([crownHill, rubyHill]);
  var satellite = L.tileLayer(mapboxUrl, {
    id: "MapID",
    tileSize: 512,
    zoomOffset: -1,
    attribution: mapboxAttribution,
  });

  layerControl.addBaseLayer(satellite, "Satellite");
  layerControl.addOverlay(parks, "Parks");

  //handle click events

  function onMapClick(e) {
    alert("You clicked the map at " + e.latlng);
  }
  map.on("click", onMapClick);
});
