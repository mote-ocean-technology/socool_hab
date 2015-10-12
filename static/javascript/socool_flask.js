function contactUs() {
  window.location.href = "mailto:rdc@mote.org?subject=SO COOL Contact Us";
}

function ucwords (str) {
    str = str.toLowerCase();
    return (str + '').replace(/^([a-z])|\s+([a-z])/g, function ($1) {
        return $1.toUpperCase();
    });
}

function getGraphData(site, serial, param, expanded_def) {
  site = ucwords(site);
  $(".appsWrapper").append("<div id='chartWrapper' class='chartWrapper'></div>");
  $(".obsMap").css("display", "none");
  $(".chartWrapper").css("display", "block");

 //Need to get data here via AJAX
//No other reasonable way to do this...
//
   $.ajax({
    url: $SCRIPT_ROOT + "/plots/" + site + "/" + param,
    success: function(data) {
      var returnedData = JSON.parse(data);
      drawPlot(returnedData, site, serial, expanded_def, param)
    }
  });
}

function drawPlot(opdData, site, serial, expanded_def, param) {
  var chart = new Highcharts.Chart({
       chart: {
            type: 'line',
            renderTo: 'chartWrapper',
            zoomType: 'xy'
        },

        title: {
          text: site + " " + expanded_def
        },
        subtitle: {
            text: "Serial #" + serial
        },
        xAxis: {
            title: {
                enabled: true,
                text: 'Date/Time'
            },

            type: 'datetime',
            labels: {
              rotation: -90
            },
            dateTimeLabelFormats: {
              month: '%b-%d',
              week: '%b-%d',
              day: '%b-%d',
              hour: '%b-%d %H:%M',
              minute: '%H:%M',
              second: '%H:%M'
            },

            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: expanded_def
            }
         },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },

        series: [{
            name: expanded_def,
            color: 'rgba(0, 0, 255, .8)',
            data: opdData,
        }],

    exporting: {
    buttons: {
      contextButton: {
        enabled: true,
        text: 'Download'
      },
      customButton: {
        x: -150,
        onclick: function () {
          $('.chartWrapper').empty();
          $('.chartWrapper').remove();
          $(".obsMap").css("display", "block");
          },
          symbol: 'square',
          symbolStrokeWidth: 2,
          symbolFill: '#ff0000',
          text: 'Close Plot Window'
          }
        }
      }
    });
}

function showObsMap(inactive_sites, active_sites) {
  var mapCenterLat = 26.5;
  var mapCenterLon = -82.2;
  var mapOptions = {
  zoom: 8,
  center: new google.maps.LatLng(mapCenterLat, mapCenterLon)
  };

  var map_obs = new google.maps.Map(document.getElementById('obs-map'), mapOptions);
  //Here we need to get at the data in opd_sites and call inactive marker
  $.each(inactive_sites, function(index, element) {
    makeInactiveMarker(map_obs, element);
  });

  $.each(active_sites, function(index, element) {
    makeActiveMarker(map_obs, element);
  });
}

function showAuvMap(active_gliders) {
  //This shoudl eventually come from database
  var mapCenterLat = 28.52;
  var mapCenterLon = -83.399;
  var mapOptions = {
  zoom: 7,
  center: new google.maps.LatLng(mapCenterLat, mapCenterLon)
  };

  var map_auv = new google.maps.Map(document.getElementById('auv-map'), mapOptions);
  //Here we need to get at the data in opd_sites and call inactive marker

  $.each(active_gliders, function(index, element) {
    makeGliderMarker(map_auv, element);
  });
}



function makeInactiveMarker(map_obs, site) {
  var image = $SCRIPT_ROOT + '/static/images/flag_gray.png';
  var myLatLng = new google.maps.LatLng(site.latitude,site.longitude);
  var marker = new google.maps.Marker({
      position: myLatLng,
      map: map_obs,
      icon: image,
      title: site.site,
      cursor: site.site
  });
}


function makeActiveMarker(map_obs, site) {
  var mapCenterLat = 26.5;
  var mapCenterLon = -82.2;
  var mapCenter = new google.maps.LatLng(mapCenterLat, mapCenterLon);
  var image = $SCRIPT_ROOT + '/static/images/flag_green.png';
  var myLatLng = new google.maps.LatLng(site.latitude, site.longitude);
  var contentString =  "<div class='infoBox'"+
  "<p><h1 class='infoBoxTitle'>"+site.site+"</h1><hr><p>" +
  "<table class='infoBoxTable'>";

  /*We could build contentString with iteration but we want to control
  the text of the key and the order of the display. We could do this
  with expanded_defs as in BCRS but this keeps things simpler
  and eliminates another database table and the overhead of queries.
  */

  //TO DO: check readings against bounds and set span accordingly
  //TO DO: create query to give us site.deployed
  //TO DO: do the math to get site.days_wet
  //TO DO: get the <b> out of contentString and use CSS --
  //this is a remnant from old code.

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Last Report:</b></td><td class='td_infoBoxData'>"+
  site.date+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Operator:</b></td><td class='td_infoBoxData'>"+
  site.operator+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Deployed:</b></td><td class='td_infoBoxData'>"+
  site.deployed+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Days Wet:</b></td><td class='td_infoBoxData'>"+
  site.days_wet+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Serial:</b></td><td class='td_infoBoxData'>"+
  site.serial+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Target Model:</b></td><td class='td_infoBoxData'>"+
  site.target_model+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Sim Index:</b></td><td class='td_infoBoxData'>"+
  site.similarity_index+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Voltage:</b></td><td class='td_infoBoxData'>"+
  site.voltage+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Bypass Pressure:</b></td><td class='td_infoBoxData'>"+
  site.pressure_drop+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>CDOM Ref(ml):</b></td><td class='td_infoBoxData'>"+
  site.water_vol+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Integration Time:</b></td><td class='td_infoBoxData'>"+
  site.integration_time+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Status Code:</b></td><td class='td_infoBoxData'>"+
   site.error_code+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>Slope:</b></td><td class='td_infoBoxData'>"+
  site.cdom_slope+"</td></tr>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>"+
  "<b>a(440) Intercept:</b></td><td class='td_infoBoxData'>"+
  site.intercept+"</td></tr>";

  contentString = contentString + "</table></div>";

  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });
  var marker = new google.maps.Marker({
      position: myLatLng,
      map: map_obs,
      icon: image,
      title: site.site,
      cursor: site.site
  });
  google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map_obs, marker);
  });
  google.maps.event.addListener(infowindow, 'closeclick', function() {
    map_obs.setCenter(mapCenter);
  });
}


function makeGliderMarker(map_auv, glider) {
  latitude = glider.latitude
  longitude = glider.longitude
  var mapCenterLat = 28.52;
  var mapCenterLon = -83.399;
  var mapCenter = new google.maps.LatLng(mapCenterLat, mapCenterLon);

  var image = 'http://coolcloud.mote.org/socool_hab/static/images/slocum-default.png'
  var myLatLng = new google.maps.LatLng(latitude, longitude);
  var contentString =  "<div class='infoBox'"+
  "<p><h1 class='infoBoxTitle'>"+glider.serial+"</h1><hr><p>" +
  "<table class='infoBoxTable'>";

  contentString = contentString + "<tr><td class='td_infoBoxSensor'>" +
"<a href=http://coolcloud.mote.org/deployments/usf-bass/plots/>" +
"<img src='{{ request.script_root }}/static/images/sci_water_temp_thumb.png'></img></a></td></tr>" +
"</tr><tr><td class='td_infoBoxSensor'><b>Click On Image For Plots</b></td></tr>"

  contentString = contentString + "</table>"

 contentString = contentString + "</div>";
  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });

  var marker = new google.maps.Marker({
      position: myLatLng,
      map: map_auv,
      icon: image,
      title: glider.serial,
      cursor: glider.serial
  });
  google.maps.event.addListener(marker, 'click', function() {
    //infowindow.open(map_auv, marker);
    onclick = window.location.assign('http://coolcloud.mote.org/deployments/usf-bass/plots');
  });
  google.maps.event.addListener(infowindow, 'closeclick', function() {
    map_auv.setCenter(mapCenter);
    map_auv.setZoom(7);
  });

}

