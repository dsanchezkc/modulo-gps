require([
    "dojo/on", //Captura eventos en objetos ejemplo onChange: function(planta){
    "dojo/mouse", // Captura eventos desde el mouse
    "dijit/layout/BorderContainer",
    "dojo/fx/Toggler", //custom animation functions
    "dojo/fx",
    "dojo/request", // Carga datos desde la url definida ejemplo: request.get(defaultUrl+ "/gps/plantas/"
    "dojo/store/Memory", // usado adaptar datos obtenidos Json ejemplo store: new Memory({ idProperty: "id", data: data }),
    "dijit/registry", //usado en la busqueda por id ejemplo: registry.byId("negocio").destroyRecursive();
    "dijit/layout/ContentPane",
    "dijit/form/DateTextBox",
    "dojo/dom",
    "dojo/dom-attr",
    "dijit/layout/AccordionContainer",
    "dojox/grid/DataGrid",
    "dijit/form/Button",
    "dojo/data/ObjectStore",
    "dojo/dom-construct", // constructor objetos ejemplo: domConstruct.toDom(" <input id='negocio' />");
    "dijit/form/FilteringSelect", // Crear desplegables con información dijit.form.FilteringSelect({
    "dojo/domReady!"
], function(on, mouse,BorderContainer,Toggler, coreFx, request, Memory, registry,ContentPane, DateTextBox,dom,domAttr,AccordionContainer,DataGrid,Button,ObjectStore, domConstruct, FilteringSelect){
    var coord = [];
    var lat=document.getElementById("lat").value;
    var lon=document.getElementById("lon").value;
    var nro=document.getElementById("nro").value;
    var nombre=document.getElementById("nombre").value;
    var apellidop=document.getElementById("apellidop").value;
    var cargo=document.getElementById("cargo").value;
    coord.CENTRAL = [lat,lon];

    var etiquetas = [];

    var defaultUrl ="http://staff.estchile.cl";
    //var defaultUrl = "localhost:8000";//local
    var defaultUrlGeoServer ="http://104.196.40.15:8080";
    var urlRealTime;

    var map = new L.Map('map', {center: coord.CENTRAL, zoom: 20});


/****TODO MAPA*****/

    var osm = new L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 22,
        minZoom:2,
        attribution: 'OpenStreetMap'
        });

    var ctb = new L.tileLayer.wms('http://demo.opengeo.org/geoserver/ows?', {
        layers: 'ne:ne_10m_admin_0_countries,ne:ne_10m_admin_0_boundary_lines_land',
        maxZoom: 30,
        minZoom:2,
        attribution: 'OpenStreetMap'
        });

    var zonas = new L.LayerGroup();

     var ggl = new L.Google('SATELLITE', {
            mapOptions: {
            //styles: styles
        }});

    var overlays = {//Capa con marcadores
            "Zonas": zonas
        };

    map.addLayer(ggl);
    /*lcontrol = L.control.layers({'OSM':osm,
        'Google':ggl,
        'Countries, then boundaries':ctb
    }, overlays).addTo(map);
    */
    lcontrol = L.control.layers({
        'Google':ggl
    }, overlays).addTo(map);

    /**********************************/
    function getColor(d) { //retorna un color de acuerdo al valor de la variable d (density) ojo tambien se usa para el color de la leyenda
        //console.log(d);
        return d > 5 ? '#800026' :
               d > 4  ? '#E31A1C' :
               d > 3  ? '#FC4E2A' :
               d > 1   ? '#FED976' :
                        '#FFEDA0';
    }

    function style(feature) { //asigna el estilo con el color de relleno de acuerdo a su densidad
        return {
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7,
            fillColor: getColor(feature.properties.nivel_riesgo)
        };
    }

    //var marker = L.marker(coord.CENTRAL).bindPopup("<p><b>Nombre: </b>"+nombre+" "+apellidop+"<br><b>Cargo:</b>"+cargo+"<br><b>Teléfono: </b>"+nro+ "</p>").addTo(map);
    //var marker = L.marker(coord.CENTRAL);
    var leyenda= "<div id='wrapperCard'><img id='logoEstCard' src='/static/images/estchile.png' ><img id='imgQRCard' src='/static/images/estchile.png' ><div id='datosTrabajadorCard'><b>Nombre : </b>"+
                nombre+" "+apellidop +"</br><b>Cargo : </b>"+
                cargo+
                "</br><b>Fono : </b>"+
                "<a href='tel:"+nro+"'>"+nro+"</a>"+
                "</br><b>Fono Emergencia : </b>"+
                "<a href='tel:"+fonoem+"'>"+fonoem+"</a>"+
                "</br><b>Contacto : </b>"+
                nombre+ "</div>";//+"</br></div><img id='imgTrabajadorCard' src="+defaultUrl+f.properties["foto"]+"></div>";
    //l.bindPopup(leyenda);

    var tempIcon;

    if(nro >= 5 ){
        //l.setIcon(hombreRojo);
        //out2.push( "<p>"+f.properties["nombre"]+"</p>");
        tempIcon = hombre5;
    }
    else if(nro == 4 ){
        tempIcon = hombre4;
    }
    else if(nro == 3 ){
        tempIcon = hombre3;
    }
    else if(nro == 2 ){
        tempIcon = hombre2;
    }
    else {
        tempIcon = hombre1;
    }

    //l.setIcon(tempIcon);


    //l.addTo(trabajadores);

    function popUpEdificios(f,l){
        var out = [];
        if (f.properties){
            for(key in f.properties){
                out.push( "<b>"+  key+"</b>"+" : "+f.properties[key]);
            }
            l.bindPopup(out.join("<br />"));
        }
        l.addTo(zonas);

                var label = new L.Label();
        label.setContent(f.properties["nombre"]);
        //console.log(f.properties["nombre"]);
        label.setLatLng(l.getBounds().getCenter());


        etiquetas.push(label);
    }

    /********ICONOS PERSONALIZADO***************/
    var LeafIcon = L.Icon.extend({
                options: {
                    //shadowUrl: '/static/images/leaf-shadow.png',
                    iconSize:     [25, 50],
                    //shadowSize:   [50, 64],
                    iconAnchor:   [12, 50],
                    //shadowAnchor: [4, 62],
                    popupAnchor:  [0, -46]
                }
            });

    var hombre1 = new LeafIcon({iconUrl: '/static/images/ico/marker-1.png'}),
        hombre2 = new LeafIcon({iconUrl: '/static/images/ico/marker-2.png'}),
        hombre3 = new LeafIcon({iconUrl: '/static/images/ico/marker-3.png'}),
        hombre5 = new LeafIcon({iconUrl: '/static/images/ico/marker-5.png'}),
        hombre4 = new LeafIcon({iconUrl: '/static/images/ico/marker-4.png'});

    var showcluster=false;
    var urlRealTime = defaultUrl+"/gps/puntos3/";
    //var urlEdificios= "../../static/home/edificio.json";
    var urlEdificios= "/static/edificios.json";

    var jsonTest = new L.GeoJSON.AJAX([urlEdificios/*,"counties.geojson"*/],{style: style, onEachFeature:popUpEdificios});

    map.on('overlayadd', function(eo) {
        //console.log("Activado "+ eo.name);
        if (eo.name === 'Zonas') {
                    //console.log(etiquetas);
            for (var i = 0, l = etiquetas.length; i < l; ++i) {
                //console.log(etiquetas[i]);
                //tempLabel = etiquetas[i];
                map.showLabel(etiquetas[i]);
            }
        }
    });




    map.on('zoomend', function () {
        if (map.getZoom() > 21 && map.hasLayer(osm))        {
            map.removeLayer(osm);
            map.addLayer(ctb);
        }
        else if (map.getZoom() > 18 && map.hasLayer(ggl)) {
            map.removeLayer(ggl);
            map.addLayer(osm);
        }

        if (map.getZoom() < 19 && map.hasLayer(ctb)|| map.getZoom() < 19 && map.hasLayer(osm))
        {
            map.removeLayer(ctb);
            map.removeLayer(osm);
            map.addLayer(ggl);
        }


    });
     L.marker(coord.CENTRAL, {icon: hombre1}).addTo(map).bindPopup(leyenda).openPopup();
});
