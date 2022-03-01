window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {
        pointToLayer: function(feature, latlng, context) {
            return L.circleMarker(latlng, {fillColor : "#ff7800",color : "#000",})
        }
    }
});



//function(feature, latlng) {
//                    return L.circleMarker(latlng, {
//                        radius : 8,
//                        fillColor : "#ff7800",
//                        color : "#000",
//                        weight : 1,
//                        opacity : 1,
//                        fillOpacity : 0.8
//                    });
//                }