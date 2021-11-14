// Đầu tiên, để có thể show map thì phải xét hệ toạ độ
const extent = [632683.697, 1935379.718, 645733.697, 1962889.718];
// const extent = [200, 200, 435, 917]

var projection = new ol.proj.Projection({
    code: 'EPSG:3405',
    units: 'm',
});

var view = new ol.View({
    projection: projection,
});

var map = new ol.Map({
    layer: [],
    target: 'map',
    view: view
});

var mousePositionControl = new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(3),
    projection: projection,
    className: 'mouse-position',
    target: document.getElementById('position_mouse'),
    undefinedHTML: '&nbsp;',
})

map.addControl(mousePositionControl);
map.getView().fit(extent, map.getSize());
const _layer = new ol.layer.Image({
    source: new ol.source.ImageStatic({
        url: 'http://127.0.0.1:8000/img',
        projection: projection,
        imageExtent: extent,
    })
})

map.addLayer(_layer);