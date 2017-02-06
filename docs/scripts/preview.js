

//Filter laden
$.getJSON(url+"/filters",{},function(data){
  var counter = 0;

  $("#filters").append("<li> <div class = \"menu-space\" >");
  $.each(data, function(key, value) {
    if(counter%3 == 0 && counter != 0){
        $("#filters").append("</div></li>");
        $("#filters").append("<li> <div class = \"menu-space\" >");
    }

    $("#filters").append(""+
      "<div class = \"menu-item\" id = \""+value[0]+"-"+value[1]+"\" onclick=\"applyFilter(\'"+value[0]+":"+value[1]+"\')\">"+
      "        <div class = \"menu-image\">"+
              "<img src = \"img/preview/filters/"+value[3]+"\" class = \"preview-image\">"+
            "</div>"+
          "<div class = \"menu-description\">"+value[2]+"</div>"+
      "</div>");




   console.log(key+ counter + value[3]);
   counter = counter + 1;
  });
  for(var i = 0; i < 2-(counter-1)%3; i++){
    $("#filters").append("<div class = \"menu-item space\"></div>");

  }

  $("#filters").append(" </div></li> <li><a>Filter</a></li>");

  //Aktiven Filter Laden
  $.get(url+"/stream/12345/filteractive",function(data){
    var lastFilter = data;
    console.log(lastFilter);
      $("#"+lastFilter).addClass("menu-item-selected");
    });


});

//Masken Laden

$.getJSON(url+"/masks",{},function(data){
  var counter = 0;

  $("#masks").append("<li> <div class = \"menu-space\" >");
  $.each(data, function(key, value) {
    if(counter%3 == 0 && counter != 0){
        $("#masks").append("</div></li>");
        $("#masks").append("<li> <div class = \"menu-space\" >");
    }

    $("#masks").append(""+
      "<div class = \"menu-item\"  id = \""+value[0]+"-"+value[1]+"\" onclick=\"applyMask(\'"+value[0]+":"+value[1]+"\')\">"+
      "        <div class = \"menu-image\">"+
              "<img src = \"img/preview/masks/"+value[3]+"\" class = \"preview-image\">"+
            "</div>"+
          "<div class = \"menu-description\">"+value[2]+"</div>"+
      "</div>");




   console.log(key+ counter + value[3]);
   counter = counter + 1;
  });
  for(var i = 0; i < 2-(counter-1)%3; i++){
    $("#masks").append("<div class = \"menu-item space\"></div>");

  }

  $("#masks").append(" </div></li> <li><a>Masken</a></li>");

  //Aktive Maske laden
  $.get(url+"/stream/12345/maskactive",function(data){
    var lastMask = data;
    console.log(lastMask);
      $("#"+lastMask).addClass("menu-item-selected");
    });


});


//Kameras laden
$.getJSON(url+"/stream/12345/cams",{},function(data){



  $.each(data, function(key, value) {

      $("#cams").append("<li><a onClick=\"changeCam("+value+")\">"+key+"</a></li>");


});


  });

//Stream Starten

function initialise(){



  $('.stream').css('background-image','url(/stream/12345/image)');
    $('body').css('background-image','none');


}


//Fullscreen

isFullscreen = true;

function fullscreen(){
  if(isFullscreen){



          $('.stream').css('background-image','url(/stream/12345/image)');

                $('.stream').css('background-size','contain');

  }else {

    $('.stream').css('background-image','url(/stream/12345/image)');
      $('.stream').css('background-size','cover');


  }
  isFullscreen = !isFullscreen;

}
