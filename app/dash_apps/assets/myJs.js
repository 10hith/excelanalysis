//window.myNamespace = Object.assign({}, window.myNamespace, {
//    mySubNamespace: {
//        pointToLayer: function (feature, latlng, context) {
//            const greenIcon = L.icon({
//                iconUrl: 'https://raw.githubusercontent.com/10hith/excelanalysis/release/aio/app/dash_apps/assets/favicon.ico',                iconSize: [20, 15], // size of the icon
//                shadowSize: [20, 15], // size of the shadow
//                iconAnchor: [20, 15], // point of the icon which will correspond to marker's location
//                shadowAnchor: [4, 62],  // the same for the shadow
//                popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
//            });
//            return L.marker(latlng, {icon: greenIcon})
//        }
//    }
//});


window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {
        pointToLayer: function (feature, latlng, context) {
            const greenIcon = L.icon({
                iconUrl: 'https://raw.githubusercontent.com/10hith/excelanalysis/release/aio/app/dash_apps/assets/favicon.ico',                iconSize: [20, 15], // size of the icon
                shadowSize: [20, 15], // size of the shadow
                iconAnchor: [20, 15], // point of the icon which will correspond to marker's location
                shadowAnchor: [4, 62],  // the same for the shadow
                popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
            });
            return L.marker(latlng, {icon: greenIcon})
        }
    }
});