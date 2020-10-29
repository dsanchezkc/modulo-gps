//version 05/07/16 15.17 hrs
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
    var heat_points = [];
    //coordenadas de interes...
    var coord = [];
    coord.CENTRAL = [-36.3,-72.3]; //Posicion inicial para centrar el mapa

    var out2 = [];//Cadena para concatenar la informacion de los trabajadores en riesgo

    var defaultUrl ="http://staff.estchile.cl"; //URL con la que se va a trabajar
    //var defaultUrl = "localhost:8000";//local


    var urlRealTime; // Url de la direccion del Json con la informaicon de todos los trabajadores

	var map = new L.Map('map', {center: coord.CENTRAL, zoom: 2}); //inicializacion del mapa

    // MOSTRAR OCULTAR PANEL LATERAL

    var togglerRightPanel = new Toggler({
        node: "rightPanel",
        showFunc: coreFx.wipeIn,
        hideFunc: coreFx.wipeOut
    });

    on(dom.byId("hideButton"), "click", function(e){
        togglerRightPanel.hide();
    });

    on(dom.byId("showButton"), "click", function(e){
        togglerRightPanel.show();

    });

    statusOk = function(){ //Funcion para alternar el color del mensaje de aviso
      dojo.animateProperty({
        node: dojo.byId("aviso"), duration: 2000,
        properties: {
          backgroundColor: { start: "yellow", end: "red" },
          //height: { end: 400, start:100 },
          color: { start: "black", end: "white" },
        },
        onEnd: function(){
          //dojo.byId("aviso").innerHTML = "Granted";
        }
      }).play();
    }
    /*Lista de Desplegables*/
    /* Lectura archivo Json Plantas*/
    request.get(defaultUrl+ "/gps/plantas/", {
            handleAs: "json"
        }).then(function(data){
            new dijit.form.FilteringSelect({
            id: "planta",
            store: new Memory({ idProperty: "id", data: data }),
            autoComplete: true,
            //value: data[0].id,
            style: "width: 165px; margin-top: 5px;",
            onChange: function(planta){
                var posicion = dijit.byId('planta').get('value');
                var zoom;
                if(data[posicion].name=== "Todos"){zoom=5;}
                else {zoom= 17;}

                map.setView([data[posicion].lat,data[posicion].lon], zoom);
                //alert(dijit.byId('planta').get('value'));
                //alert(dijit.byId('planta').get('displayedValue'));

                /* Lectura archivo Json Negocios*/
                var cn= dijit.byId('planta').get('displayedValue');

                request.get(defaultUrl+ "/gps/centrosdenegocio/"+cn+"/", {
                        handleAs: "json"
                    }).then(function(data){
                        /* Funcion Buscar si existe registro en caso afirmativo lo elimina
                        de lo contrario lo crea*/
                        if(typeof registry.byId("negocio") != "undefined"){
                            registry.byId("negocio").destroyRecursive();
                        }
                        var row = domConstruct.toDom(" <input id='negocio' />");
                            domConstruct.place(row, "CN"); // "CN" es la id donde se creará "row"

                        new dijit.form.FilteringSelect({
                            id: "negocio",
                            store: new Memory({idProperty:"id", data: data }),
                            autoComplete: true,
                            style: "width: 165px; margin-top: 5px;",
                            required: true,
                            //value: data[0].id,
                            searchAttr: "name",
                            onChange: function(negocio){
                                //urlRealTime = "http://localhost:8000/gps/trabajadores/CMMA01/puntos2/";

                                /* Funcion Buscar si existe registro en caso afirmativo lo elimina
                                de lo contrario lo crea*/

                                if(typeof registry.byId("trabajador") != "undefined"){
                                    registry.byId("trabajador").destroyRecursive();
                                }
                                var row = domConstruct.toDom(" <input id='trabajador' />");
                                    domConstruct.place(row, "TB"); // "TB" es la id donde se creará "row"

                                /* Lectura archivo Json Trabajadores*/

                                //
                                var tb= dijit.byId('negocio').get('Value');
                                var url2= defaultUrl+ "/gps/trabajadores/"+tb+"/";
                                //console.log(url2);
                                request.get(url2, {
                                    handleAs: "json"
                                }).then(function(data){
                                /*
                                //Validación de Datos Vacios
                                console.log(data[0]);
                                //console null validar
                                if(data[0]){
                                    console.log("NO VACIO");
                                }
                                else{
                                    //console.log("VACIO");
                                    data = [{'i': 0, 'lat': -36.198815, 'lon': -71.8265844444444, 'name':' sin trabajador', 'id': 0}];
                                }
                                console.log(data);
                                */
                                    new dijit.form.FilteringSelect({
                                        id: "trabajador",
                                        store: new Memory({idProperty: "id", data: data }),
                                        autoComplete: true,
                                        style: "width: 165px; margin-top: 5px;",
                                        //value: data[0].id,
                                        onChange: function(trabajador){
                                            /*console.log(data[0]);
                                            //console null validar
                                            if(data[0]){
                                                console.log("NO VACIO");

                                            }
                                            else{
                                                console.log("VACIO");
                                                //data = "[{'i': 1, 'lat': -36.198815, 'lon': -71.8265844444444, 'name':' sin trabajador', 'id': 0}]";
                                            }*/


                                            var posicion = dijit.byId('trabajador').get('value');
                                            //map.setView([data[posicion].lat,data[posicion].lon], 18);
                                           /***FUNCION POSICION ACTUALIZADA FUNCIONAL PERO EXISTE TIEMPO DE ESPERA***/
                                            //alert(dijit.byId('trabajador').get('value'));
                                            //console.log(data);
                                            var url3= defaultUrl+ "/gps/trabajador/"+data[posicion].i+"/";
                                            //console.log(url3);
                                            request.get(url3, {
                                                    handleAs: "json"
                                                }).then(function(data2){
                                                        //console.log(data2)
                                                        //console.log(data2.features);
                                                        //console.log(data2.features[0].properties.lat);
                                                        map.setView([data2.features[0].properties.lat,data2.features[0].properties.lon], 18);
                                            });

                                            /**********************/
                                            //.openPopup()

                                            // Mediante un ciclo buscar el marcador con la propiedad nombre igual a la de arriba para desplegar su popUp

                                        }
                                    }, "trabajador").startup();
                            });
                            }
                        }, "negocio").startup();
                });
            }
        }, "planta").startup();
    });
    /*Fin Listas Desplegables*/


    var urlINFORME;

    /*consulta informes*/
    /* Lectura archivo Json Plantas*/
    request.get(defaultUrl+ "/gps/plantas/", {
            handleAs: "json"
        }).then(function(data){
            new dijit.form.FilteringSelect({
            id: "planta2",
            store: new Memory({ idProperty: "id", data: data }),
            autoComplete: true,
            //value: data[0].id,
            style: "width: 165px; margin-top: 5px;",
            onChange: function(planta2){
                var posicion = dijit.byId('planta2').get('value');
                /* Lectura archivo Json Negocios*/
                var cn= dijit.byId('planta2').get('displayedValue');
                request.get(defaultUrl+ "/gps/centrosdenegocio/"+cn+"/", {
                        handleAs: "json"
                    }).then(function(data){
                        /* Funcion Buscar si existe registro en caso afirmativo lo elimina
                        de lo contrario lo crea*/
                        if(typeof registry.byId("negocio2") != "undefined"){
                            registry.byId("negocio2").destroyRecursive();
                        }
                        var row = domConstruct.toDom(" <input id='negocio2' />");
                            domConstruct.place(row, "CN2"); // "CN" es la id donde se creará "row"

                        new dijit.form.FilteringSelect({
                            id: "negocio2",
                            store: new Memory({idProperty:"id", data: data }),
                            autoComplete: true,
                            style: "width: 165px; margin-top: 5px;",
                            required: true,
                            //value: data[0].id,
                            searchAttr: "name",
                            onChange: function(negocio2){
                                /* Funcion Buscar si existe registro en caso afirmativo lo elimina
                                de lo contrario lo crea*/

                                if(typeof registry.byId("trabajador2") != "undefined"){
                                    registry.byId("trabajador2").destroyRecursive();
                                }
                                var row = domConstruct.toDom(" <input id='trabajador2' />");
                                    domConstruct.place(row, "TB2"); // "TB" es la id donde se creará "row"

                                /* Lectura archivo Json Trabajadores*/
                                //
                                var tb= dijit.byId('negocio2').get('Value');
                                var url2= defaultUrl+ "/gps/trabajadores/"+tb+"/";
                                request.get(url2, {
                                    handleAs: "json"
                                }).then(function(data){
                                    new dijit.form.FilteringSelect({
                                        id: "trabajador2",
                                        store: new Memory({idProperty: "id", data: data }),
                                        autoComplete: true,
                                        style: "width: 165px; margin-top: 5px;",
                                        //value: data[0].id,
                                        onChange: function(trabajador2){

                                            var posicion = dijit.byId('trabajador2').get('value');
                                            //map.setView([data[posicion].lat,data[posicion].lon], 18);
                                            /***FUNCION POSICION ACTUALIZADA FUNCIONAL PERO EXISTE TIEMPO DE ESPERA***/
                                            //alert(dijit.byId('trabajador').get('value'));
                                            //console.log(data);
                                            var url3= defaultUrl+ "/gps/trabajador/"+data[posicion].i+"/";
                                            //console.log(url3);
                                            request.get(url3, {
                                                    handleAs: "json"
                                                }).then(function(data2){
                                                        //console.log(data[0].lat);
                                                         map.setView([data2.features[0].properties.lat,data2.features[0].properties.lon], 18);

                                            });

                                            /**********************/
                                            urlINFORME = defaultUrl+"/gps/datosinforme/"+cn+"/02/"+data[posicion].i+"/";

                                        }
                                    }, "trabajador2").startup();
                            });
                            }
                        }, "negocio2").startup();
                });
            }
        }, "planta2").startup();
    });
    /*Fin Listas Desplegables*/

    /* Informe Fecha */

    on(document.getElementById("qwerty"), "click", function(e){
            if(typeof registry.byId("gridDiv") != "undefined"){
                    registry.byId("gridDiv").destroyRecursive();
                }
            var row = domConstruct.toDom("<div id='gridDiv'>    </div>");
                    domConstruct.place(row, "divFecha");
            var grid, dataStore;
            var fechaFF,fechaII;

            // get value
            fechaII = date1.value
            //fechaII = "2016-03-01";
            fechaFF = date2.value
            //fechaFF = "2016-09-10";
            var url3 = urlINFORME+ fechaII +"/"+ fechaFF+"/";

            request.get(url3, {
                handleAs: "json"
            }).then(function(data){
                dataStore =  new ObjectStore({ objectStore:new Memory({ data: data }) });
                grid = new DataGrid({
                    store: dataStore,
                    query: { id: "*" },
                    queryOptions: {},
                    structure: [//nombre columnas
                        { name: "Nombre", field: "name", width: "50%" },
                        { name: "Tiempo", field: "id", width: "25%" }
                        //{ name: "Horas", field: "horas", width: "25%" },
                        //{ name: "Minutos", field: "minutos", width: "25%" }
                    ]
                }//).placeAt("gridDiv");
                ,"gridDiv");
                grid.startup();
            });
            console.log(url3);
    });

/****TODO MAPA*****/

    PruneCluster.Cluster.ENABLE_MARKERS_LIST = true;
    var leafletView = new PruneClusterForLeaflet();



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
    var alertaL = new L.LayerGroup();
    var heatMap = new L.LayerGroup();
    var etiquetasL = new L.LayerGroup();
    var etiquetas = [];

    var markerTrabajador = new L.LayerGroup();
    var trabajadores = new L.LayerGroup();

    var ggl = new L.Google('SATELLITE', {
            mapOptions: {
            //styles: styles
        }});

    var overlays = {//Capa con marcadores
            "Trabajadores": trabajadores,
            "Cluster": markerTrabajador,
            "Zonas": zonas,
            //"Heat Map": heatMap,
            "Activar Alerta": alertaL,
            "Activar Etiquetas": etiquetasL

        };

    //map.addLayer(alertaL)
    var activarAlerta=false;

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

    function style(feature) { //asigna el estilo con el color de relleno de acuerdo a su nivel de riesgo
        return {
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7,
            fillColor: getColor2(feature.properties.nivel_riesgo)
        };
    }

    function popUpPersona(f,l){//Consulta por cada uno de los objetos
        //console.log(f.geometry.coordinates);//
        //console.log(l);

        //var tempLatLng =l.getLatLng();
        //map.setView([tempLatLng.lat,tempLatLng.lng], 18);
/*test popUp boton setView
        l.bindPopup("<button type='button' id='otroButton'>Mostrar Información </button><div id='wrapperCard'><img id='logoEstCard' src='/static/images/estchile.png' ><img id='imgQRCard' src='/static/images/estchile.png' ><div id='datosTrabajadorCard'><b>Nombre : </b>"+f.properties["nombre"]+"</br><b>Cargo : </b>"+f.properties["cargo"]+"</br><b>Fono : </b>"+f.properties["fono"]+"</br><b>Riesgo : </b>"+f.properties["nivel_riesgo"]+"</br><b>Fono Emergencia : </b>"+f.properties["nro_emergencia"]+"</br><b>Contacto : </b>"+f.properties["tipo_contacto"]+"</br></div><img id='imgTrabajadorCard' src="+defaultUrl+f.properties["foto"]+"></div>");
*/
        //l.bindPopup("<div id='wrapperCard'><img id='logoEstCard' src='/static/images/estchile.png' ><img id='imgQRCard' src='/static/images/estchile.png' ><div id='datosTrabajadorCard'><b>Nombre : </b>"+f.properties["nombre"]+"</br><b>Cargo : </b>"+f.properties["cargo"]+"</br><b>Fono : </b>"+f.properties["fono"]+"</br><b>Riesgo : </b>"+f.properties["nivel_riesgo"]+"</br><b>Fono Emergencia : </b>"+f.properties["nro_emergencia"]+"</br><b>Contacto : </b>"+f.properties["tipo_contacto"]+"</br></div><img id='imgTrabajadorCard' src="+defaultUrl+f.properties["foto"]+"></div>");

        //l.setIcon(hombreNormal);
        var tempRiesgo = f.properties["nivel_riesgo"];
        var tempLatLng =l.getLatLng(); //PARA HEATMAP
        heat_points.push(tempLatLng);
        var tempIcon;
        //console.log(f.properties["zona"]);
        if(tempRiesgo >= 5 ){
            tempRiesgo = 5;
            //l.setIcon(hombreRojo);
            if(f.properties["zona"])
                {
                    var tempZona= f.properties["zona"];

                    //+"/gps/sms/"+f.properties["fono"]
                    out2.push( "<a href='"+defaultUrl+"/gps/sms/"+f.properties["fono"]+"' target='_self'><p>"+f.properties["nombre"]+" - "+f.properties["zona"]+"</p></a>");
                }
            else
                {
                    out2.push( "<a href='"+defaultUrl+"/gps/sms/"+f.properties["fono"]+"' target='_self'><p>"+f.properties["nombre"]+"</p></a>");
                    var tempZona= "Sin Información";
            }
            tempIcon = hombre5;
            //leafletView.RegisterMarker(new PruneCluster.Marker(tempLatLng.lat, tempLatLng.lng, {title: leyenda, icono: hombreRojo}));

        }
        else if(tempRiesgo == 4 ){
            tempIcon = hombre4;
        }
        else if(tempRiesgo == 3 ){
            tempIcon = hombre3;
        }
        else if(tempRiesgo == 2 ){
            tempIcon = hombre2;
        }
        else {
            tempIcon = hombre1;
        }

        var leyenda= "<div id='wrapperCard'><img id='logoEstCard' src='/static/images/estchile.png' ><img id='imgQRCard' src='/static/images/estchile.png' ><div id='datosTrabajadorCard'><b>Nombre : </b>Densímetro Nuclear #ID123</br><b>Modelo : </b>Troxler modelo 3230</br><b>Fono Emergencia: </b>993194369</br><b>Riesgo : </b>Alto</br><b>Fono Emergencia : </b>6003607777</br><b>Zona : </b>Almacenaje</br><a href='http://staff.estchile.cl/est/machine/3/'>Url Información</a><b>Actualizado : </b>"+f.properties["fixtime"]+"</br></div><img id='imgTrabajadorCard' src='https://img.wikicharlie.cl/thumb/9/9d/Densimetro_Nuclear_WikicharliE.jpg/300px-Densimetro_Nuclear_WikicharliE.jpg'></div>";
        l.bindPopup(leyenda);


        l.setIcon(tempIcon);
        var m = new PruneCluster.Marker(tempLatLng.lat, tempLatLng.lng, {title: leyenda,  icono: tempIcon},tempRiesgo);


        leafletView.RegisterMarker(m);

        l.on('dblclick', onClick);
        l.addTo(trabajadores);

    }

    function onClick(e) {
        var tempLatLng =this.getLatLng();
        map.setView([tempLatLng.lat,tempLatLng.lng], 18);
        //map.removeControl();
    }

    function popUpEdificios(f,l){
        var out = [];
        if (f.properties){
            for(key in f.properties){
                out.push( "<b>"+  key+"</b>"+" : "+f.properties[key]);
            }
            l.bindPopup(out.join("<br />"));
        }

        var label = new L.Label();
        label.setContent(f.properties["nombre"]);
        //console.log(f.properties["nombre"]);
        label.setLatLng(l.getBounds().getCenter());

        //map.showLabel(label);
        l.addTo(zonas);
        //map.hideLabel(label);

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
    var example= "/static/example.json";
    realtime = L.realtime({
            url: example,
            crossOrigin: true,
            type: 'json'
        },
        {
            interval: 30 * 1000
            //,
            //onEachFeature:popUpPersona
        }
        );

    realtime.on('update', function(e){
        //console.log(leafletView);
        var temp = [];
        var urlRealTime = defaultUrl+"/gps/puntos3/";//Redefinir la url porque por lo visto funciona como variable local
        //console.log(heat_points);
        trabajadores.clearLayers();
        var jsonTrabajadores = new L.GeoJSON.AJAX([urlRealTime/*,"counties.geojson"*/],{onEachFeature:popUpPersona});
        //console.log(out2.length);
        if(showcluster===true){
            leafletView.ProcessView();
            setTimeout(function(){map.addLayer(leafletView)}, 10);
            leafletView.ProcessView();
            //setTimeout(function(){leafletView.Cluster._markers = []}, 100);
        }

        leafletView.Cluster._markers = [];
        if(out2.length>0 && activarAlerta == true) {
            document.getElementById("divALERTAS").innerHTML = "<div id='aviso'><img id='alertaImg' src='/static/images/ico/aviso.png'><h2>¡¡ALERTA!!</h1>"+out2+"</div> ";
            statusOk();
        }
        else{
            document.getElementById("divALERTAS").innerHTML = "<div id=''></div> ";
        }
        out2= temp;
    });

/*
    leafletView.PrepareLeafletMarker = function (marker, data) {
        if (marker.getPopup()) {
            marker.setPopupContent(data.title);
        } else {
            marker.bindPopup(data.title);
        }
        marker.setIcon(data.icono);

        marker.category = 5;
    };
*/

    //var urlGeoserverEdificios= defaultUrlGeoServer+"/geoserver/est40516/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=est40516:est_zona&maxFeatures=50&outputFormat=application%2Fjson";
    var urlEdificios= "/static/edificios.json";


    var jsonTest = new L.GeoJSON.AJAX([urlEdificios/*,"counties.geojson"*/],{style: style, onEachFeature:popUpEdificios});

    map.on('overlayadd', function(eo) {
        //console.log("Activado "+ eo.name);

        var tempLabel = new L.Label();
        if (eo.name === 'Cluster') {
            setTimeout(function(){map.addLayer(leafletView)}, 10);
            leafletView.ProcessView();
            setTimeout(function(){map.removeLayer(trabajadores)}, 10);
            showcluster= true;

            setTimeout(function(){legend.addTo(map)}, 10);



        }
        else if (eo.name === 'Trabajadores') {

            setTimeout(function(){map.removeLayer(markerTrabajador)}, 10);
            //leafletView.Cluster._markers = [];
            setTimeout(function(){map.removeLayer(leafletView)}, 10);
            showcluster=false;
            setTimeout(function(){legend.addTo(map)}, 10);
        }
        else if (eo.name === 'Activar Alerta') {
            activarAlerta=true;
            if(out2.length>0) {
                document.getElementById("divALERTAS").innerHTML = "<div id='aviso'><img id='alertaImg' src='/static/images/ico/aviso.png'><h2>¡¡ALERTA!!</h1>"+out2+"</div> ";
                statusOk();
            }
        }
        else if (eo.name === 'Heat Map') {

            /**********HEATMAP************/
            /*var heat = L.heatLayer(heat_points, {radius: 100,
                blur:10,
                maxZoom:2,
                opacity: 0.8
            }).addTo(map);
*/
            /*********Fin HEATMAP*******/
        }
        else if (eo.name === 'Activar Etiquetas') {
                    //console.log(etiquetas);
            for (var i = 0, l = etiquetas.length; i < l; ++i) {
                //console.log(etiquetas[i]);
                //tempLabel = etiquetas[i];
                map.showLabel(etiquetas[i]);
            }
        }
    });

     map.on('overlayremove', function(eo) {
        //console.log("Quitado "+eo.name);
        if (eo.name === 'Cluster') {
            setTimeout(function(){map.removeLayer(markerTrabajador)}, 10);
            //leafletView.Cluster._markers = [];
            setTimeout(function(){map.removeLayer(leafletView)}, 10);
            showcluster= false;
            if (legend != undefined) {
                legend.removeFrom(map);
            }
        }
        else if (eo.name === 'Trabajadores') {
            showcluster=true;
            if (legend != undefined) {
                legend.removeFrom(map);
            }
        }
        else if (eo.name === 'Activar Alerta') {
            activarAlerta=false;
            document.getElementById("divALERTAS").innerHTML = "<div id=''></div> ";
        }
        else if (eo.name === 'Heat Map') {
            location.reload();//solucion preliminar desactivar heatmap
        }
        else if (eo.name === 'Activar Etiquetas') {
                    //console.log(etiquetas);
            for (var i = 0, l = etiquetas.length; i < l; ++i) {
                //console.log(etiquetas[i]);
                //tempLabel = etiquetas[i];
                map.removeLayer(etiquetas[i]);
            }
        }

    });

    map.on('zoomend', function () {
        if (map.getZoom() > 21 && map.hasLayer(osm))
        {
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
        if (map.getZoom() < 14 && map.hasLayer(etiquetasL)) {
            map.removeLayer(etiquetasL);
        }

    });
  var colors = ['#2c9223', '#2c9223', '#0096e4', '#999900', '#ffa200', '#ff0000', '#ff0000', '#ff0000'];
  leafletView.BuildLeafletClusterIcon = function(cluster) {
            var e = new L.Icon.MarkerCluster();

            e.stats = cluster.stats;
            e.population = cluster.population;
            return e;
        };


        pi2 = Math.PI * 2;

        L.Icon.MarkerCluster = L.Icon.extend({
            options: {
                iconSize: new L.Point(120, 120),
                className: 'prunecluster leaflet-markercluster-icon'
            },

            createIcon: function () {
            // based on L.Icon.Canvas from shramov/leaflet-plugins (BSD licence)
            var e = document.createElement('canvas');
            this._setIconStyles(e, 'icon');
            var s = this.options.iconSize;

            if (L.Browser.retina) {
                e.width = s.x + s.x;
                e.height = s.y + s.y;
            } else {
                e.width = s.x;
                e.height = s.y;
            }

            // this.draw(e.getContext('2d'), s.x, s.y);
            this.draw(e.getContext('2d'), e.width, e.height);
            return e;
        },

        createShadow: function () {
            return null;
        },

        draw: function(canvas, width, height) {
            var xa = 2, xb = 50, ya = 18, yb = 21;

            //var r =  ya + (this.population - xa) * ((yb - ya) / (xb - xa));
            var r =  40;
            var radiusMarker =  r,//Math.min(r, 21),
            radiusCenter = 100,
            center = width / 2;

            if (L.Browser.retina) {
                canvas.scale(2, 2);
                center /= 2;
                canvas.lineWidth = 0.5;
            }

            canvas.strokeStyle = 'rgba(0,0,0,0.25)';

            var start = 0, stroke = true;
            for (var i = 0, l = colors.length; i < l; ++i) {
                var size = this.stats[i] / this.population;
                if (size > 0) {
                    stroke = size != 1;
                    canvas.beginPath();
                    canvas.moveTo(center, center);
                    canvas.fillStyle = colors[i];
                    var from = start + 0.10,
                    to = start + size * pi2;

                    if (to < from || size == 1) {
                        from = start;
                    }
                    canvas.arc(center, center, radiusMarker * 1.5 , from, to);//cluster contorno
                    start = start + size * pi2;
                    canvas.lineTo(center, center);
                    canvas.fill();
                    if (stroke) {
                        canvas.stroke();
                    }
                    canvas.closePath();
                }

            }
            if (!stroke) {
                canvas.beginPath();
                canvas.arc(center, center, radiusMarker, 0, Math.PI * 2);
                canvas.stroke();
                canvas.closePath();
            }

            canvas.beginPath();
            canvas.fillStyle = 'white';
            canvas.moveTo(center, center);
            canvas.arc(center, center, radiusMarker, 0, Math.PI * 2);//recuadro interior
            canvas.fill();
            canvas.closePath();

            canvas.fillStyle = '#454545';
            canvas.textAlign = 'center';
            canvas.textBaseline = 'middle';

            canvas.font = 'bold '+(this.population < 2 ? '12' : (this.population < 4 ? '11' : '9'))+'px sans-serif';

            canvas.fillText("Total "+ this.population, center, center, radiusCenter*2);
        }
    });


    leafletView.PrepareLeafletMarker = function (marker, data, category) {
        if (marker.getPopup()) {
            //marker.setPopupContent(data.title + " - " + category);
            marker.setPopupContent(data.title);
        } else {
            //marker.bindPopup(data.title + " - " + category);
            marker.bindPopup(data.title);
        }
        marker.setIcon(data.icono);
        //marker.weight = 100;

    };

    function getColor2(d) { //retorna un color de acuerdo al valor de la variable d (density) ojo tambien se usa para el color de la leyenda
        return d >= 5 ? colors[5] :
               d == 4  ?  colors[4] :
               d == 3   ?  colors[3] :
               d == 2   ?  colors[2] :
                            colors[1];
    }

    //Control con la leyenda
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),//crea el div "info legend"
            grades = [ 1, 2, 3, 4, 5],
            labels = [],
            from, to;
        labels.push('Riesgo :');
        for (var i = 0; i < grades.length; i++) {
            from = grades[i];
            to = grades[i + 1];
            labels.push(
                '<i style="background:'+ getColor2(from ) + '"></i> ' +
                from );

            /*labels.push(
                '<i style="background:'+ getColor2(from ) + '"></i> ' +
                from + (to ? '&ndash;' + to : '+'));*/
        }
        div.innerHTML = labels.join('<br>');
        return div;
    };
});
